import os
from config import GOOGLE_API_KEY
from gtts import gTTS
from fpdf import FPDF
from google import genai
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools import google_search
from google.genai import types  # Para criar conteúdos (Content e Part)
import gradio as gr
import speech_recognition as sr
import tempfile
import numpy as np  # Importe numpy para criar um array vazio para resetar o áudio


os.environ['GOOGLE_API_KEY'] = GOOGLE_API_KEY
client = genai.Client()
MODEL_ID = "gemini-2.0-flash"

# Variável global para armazenar a história confirmada
historia_salva = ""
historia_exibida = ""

## Função auxiliar que envia uma mensagem para um agente via Runner e retorna a resposta final
def call_agent(agent: Agent, message_text: str) -> str:
    # Cria um serviço de sessão em memória
    session_service = InMemorySessionService()
    # Cria uma nova sessão (você pode personalizar os IDs conforme necessário)
    session = session_service.create_session(app_name=agent.name, user_id="user1", session_id="session1")
    # Cria um Runner para o agente
    runner = Runner(agent=agent, app_name=agent.name, session_service=session_service)
    # Cria o conteúdo da mensagem de entrada
    content = types.Content(role="user", parts=[types.Part(text=message_text)])

    final_response = ""
    # Itera assincronamente pelos eventos retornados durante a execução do agente
    for event in runner.run(user_id="user1", session_id="session1", new_message=content):
        if event.is_final_response():
          for part in event.content.parts:
            if part.text is not None:
              final_response += part.text
              final_response += "\n"
    return final_response

def agente_criador_historia(entrada):
  contador = Agent(
      name = "agente_criador_historia",
      model = MODEL_ID,
      description = "Agente que ajuda na criação da história",
      instruction = """
      Você é um assistente que ajudará as crianças na montagem das histórias delas.
      As crianças irão contar parte da história, falarão de alguns personagens, contarão alguma situação ou apenas trechos dela. 
      Usando esses parametros que elas irão fornecer, crie novas histórias, divertidas, estilosas e aventureiras.
      As histórias não precisam ser longas, devem ter poucos paragrafos e deve ter fluidez na história.
      Seu público alvo são crianças entre 8 e 14 anos, então deve tomar cuidado com a linguagem utilizada.
      Lembre que essa história não deve ter emojis, apenas textos.
      """
  )

  historia = call_agent(contador, entrada)
  return historia

def enviar_para_gemini(complemento_historia):
    ## ---  Envia o complemento da história (juntamente com a história salva, se houver) para o Gemini.  --- ##
    global historia_salva, historia_exibida
    prompt = complemento_historia
    ##if historia_salva:
    ##    prompt = historia_salva + "\n" + complemento_historia
    nova_parte = agente_criador_historia(prompt)
    historia_exibida = (historia_exibida + "\n" + nova_parte).strip() if historia_exibida else nova_parte
    return historia_exibida # Retorna a história completa exibida


def confirmar_historia(historia_atual):
    ## ---  Acrescenta a história atual à história salva no arquivo.  --- ##
    nome_arquivo = "historia_confirmada.txt"
    with open(nome_arquivo, "w", encoding="utf-8") as f:
        f.write(historia_atual)
    return gr.update(value="") # Mensagem de confirmação e limpa input

def reconhecer_fala(audio_data):
    print(f"Dados de áudio recebidos: {audio_data}")
    r = sr.Recognizer()
    try:
        samplerate = audio_data[0]
        stereo_audio_data = audio_data[1]
        # Converter para mono (pegar apenas o primeiro canal)
        mono_audio_data = stereo_audio_data[:, 0]
        audio_bytes = mono_audio_data.tobytes()
        audio = sr.AudioData(audio_bytes, samplerate, sample_width=2)  # sample_width é 2 para int16
        texto = r.recognize_google(audio, language='pt-BR')
        return texto, gr.update(value=None) # Retorna o texto e a atualização para limpar o áudio
    except sr.UnknownValueError:
        return "Não foi possível entender o áudio.", gr.update(value=None)
    except sr.RequestError as e:
        return f"Erro ao solicitar o serviço de reconhecimento de fala; {e}", gr.update(value=None)
    except Exception as e:
        return f"Ocorreu um erro na transcrição: {e}", gr.update(value=None)

def salvar_em_pdf(historia_para_salvar):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    largura_pagina = pdf.w - 2 * pdf.l_margin
    altura_linha = 5  # Altura de cada linha de texto

    for linha_completa in historia_para_salvar.split('\n'):
        if not linha_completa:  # Lidar com linhas vazias
            pdf.ln(altura_linha)
            continue
        palavras = linha_completa.split(' ')
        linha_atual = ""
        for palavra in palavras:
            teste_linha = linha_atual + palavra + " "
            largura_texto = pdf.get_string_width(teste_linha)
            if largura_texto <= largura_pagina:
                linha_atual = teste_linha
            else:
                pdf.cell(largura_pagina, altura_linha, txt=linha_atual.strip(), ln=True)
                linha_atual = palavra + " "
        # Adicionar a última linha que sobrou
        pdf.cell(largura_pagina, altura_linha, txt=linha_atual.strip(), ln=True)

    nome_arquivo_pdf = "historia.pdf"
    caminho_pdf = os.path.join(tempfile.gettempdir(), nome_arquivo_pdf)
    pdf.output(caminho_pdf, "F")
    return caminho_pdf

def gerar_audio(texto_historia):
    tts = gTTS(text=texto_historia, lang='pt-br')
    nome_arquivo_audio = "historia.mp3"
    caminho_audio = os.path.join(tempfile.gettempdir(), nome_arquivo_audio)
    tts.save(caminho_audio)
    return caminho_audio

def ouvir_historia(texto_historia):
    tts = gTTS(text=texto_historia, lang='pt-br')
    nome_arquivo_audio = "historia_audio.mp3"
    tts.save(nome_arquivo_audio)
    return nome_arquivo_audio

if __name__ == "__main__":
    with gr.Blocks() as iface:
        audio_input = gr.Audio(sources=["microphone"], label="Clique no botão gravar e nos conte parte da sua história. \nQuando finalizar clique no botão stop e clique no botão Transcrever:")
        transcrever_button = gr.Button("Transcrever")
        input_crianca = gr.Textbox(lines=5, label="Escreva parte da sua história para criarmos ela para você.\nOu continue a que você já começou dando mais detalhes ou direção ao nosso narrodor.")
        enviar_button = gr.Button("Enviar suas Ideias para o Narrador contar a história.")
        historia_output = gr.Textbox(label="História Criada pelo Narrador", interactive=False) # Apenas leitura
        ouvir_button = gr.Button("Gerar Audio da História") # Botão para gerar o audio
        audio_output = gr.Audio(label="Reproduzir História") # Componente para reproduzir o áudio
        confirmar_button = gr.Button("Aceitar a história.")
        gerar_pdf_button = gr.Button("Gerar PDF", visible=False) # Botão para gerar PDF
        gerar_audio_button = gr.Button("Gerar Áudio", visible=False) # Botão para gerar áudio
        pdf_output = gr.File(label="Baixar PDf da História") # Componente para o download do PDF
        audio_download = gr.File(label="Baixar Áudio da História")

        def habilitar_gerar_arquivos():
            return gr.update(visible=True), gr.update(visible=True)

        transcrever_button.click(
            fn=reconhecer_fala,
            inputs=audio_input,
            outputs=[input_crianca, audio_input] # Agora 'audio_input' também é uma saída
        )

        enviar_button.click(
            fn=enviar_para_gemini,
            inputs=input_crianca,
            outputs=[historia_output]
        )

        confirmar_button.click(
            fn=confirmar_historia,
            inputs=historia_output,
            outputs=[input_crianca]
        ).then(habilitar_gerar_arquivos, outputs=[gerar_pdf_button, gerar_audio_button]) # Habilita os botões após aceitar a história

        gerar_pdf_button.click( # Ação do novo botão para gerar PDF
            fn=salvar_em_pdf,
            inputs=historia_output,
            outputs=[pdf_output] # Retorna o arquivo para o componente gr.File
        )

        gerar_audio_button.click(
            fn=gerar_audio,
            inputs=historia_output,
            outputs=[audio_download]
        )

        ouvir_button.click( # Ação do novo botão de ouvir história
            fn=ouvir_historia,
            inputs=historia_output,
            outputs=[audio_output]
        )

    iface.launch()
    
