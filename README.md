# 📖 Sistema de Criação de Histórias Interativo 📖


## Descrição

Este sistema interativo permite que crianças e adultos colaborem na criação de histórias de forma divertida e envolvente. 
A plataforma utiliza reconhecimento de voz e inteligência artificial para transformar ideias faladas ou escritas em narrativas ricas e criativas. 
Os usuários podem iterar em suas histórias, adicionando detalhes e expandindo a trama em várias etapas. 
Ao final do processo, as histórias podem ser salvas em formato PDF ou como arquivos de áudio.


## Funcionalidades

+ Entrada de Voz e Texto: Os usuários podem começar suas histórias falando no microfone 🎤 ou digitando suas ideias ⌨️.
+ Transcrição de Fala: A funcionalidade de transcrição converte a fala em texto 📝, facilitando a visualização e edição da história.
+ Geração de História com IA: O sistema utiliza o modelo de linguagem Gemini para expandir e enriquecer as ideias iniciais, criando uma narrativa coesa e envolvente.
+ Iteração da História: Os usuários podem continuar adicionando detalhes e expandindo a história em várias etapas, seja por voz ou texto, permitindo um processo de criação colaborativo com a IA.
+ Revisão e Edição: A história gerada pode ser revisada e editada no formato de texto ✍️.
+ Saída em Múltiplos Formatos: As histórias finalizadas podem ser geradas em formato PDF 📄 para leitura ou como arquivos de áudio 🎧 para ouvir.
+ Download de Arquivos: Os usuários podem baixar os arquivos PDF e de áudio gerados para seus dispositivos 📥.


## ⚙️ Instalação
Para instalar e executar o sistema, siga estas etapas:
### 1 - Clone o repositório:
  + Abra um terminal ou prompt de comando.
  + Navegue até o diretório onde você deseja salvar o projeto.
  + Clone o repositório do projeto usando o comando:
```
git clone <URL_DO_REPOSITÓRIO>
```
### 2 - Crie um ambiente virtual (recomendado):
  + Navegue até o diretório do projeto:
```
cd nome-do-repositorio
```
  + Crie um ambiente virtual:
```
python -m venv venv
```
  + Ative o ambiente virtual:
```
Linux/macOS: source venv/bin/activate
Windows:     venv\Scripts\activate
```
### 3 - Instale as dependências:
  + Com o ambiente virtual ativado, instale as dependências do projeto usando o pip:
```
pip install -r requirements.txt
```
### 4 - Configure a chave da API do Google:
  + Você precisa obter uma chave de API do Google para usar o modelo Gemini. Siga as instruções na documentação do Google Cloud para obter sua chave de API.
  + Crie um arquivo chamado config.py na raiz do projeto.
  + Adicione a seguinte linha ao arquivo config.py, substituindo <SUA_CHAVE_API> pela sua chave de API real:
```
GOOGLE_API_KEY = "<SUA_CHAVE_API>"
```
### 5 - Execute o sistema:
  + No terminal, com o ambiente virtual ativado, execute o script principal:
```
python main.py
```
### 6 - Acesse a interface no navegador:
  + O Gradio irá iniciar o sistema e exibir uma mensagem no terminal com o endereço para acessar a interface. Geralmente, será algo como:
```
Acesse a URL: http://127.0.0.1:7860
```


## Como Usar o Sistema

### 1 - Iniciar a História:
  + Use o botão "Gravar" para falar sua ideia inicial para a história. Após gravar, clique em "Transcrever".
  + Como alternativa, você pode digitar sua ideia inicial na caixa de texto fornecida.

### 2 - Enviar para o Narrador: 
  + Clique no botão "Enviar suas Ideias para o Narrador contar a história".
  + O sistema usará a IA para gerar uma parte da história com base em sua entrada.

### 3 - Revisar a História: 
  + A história gerada será exibida na caixa de texto "História Criada pelo Narrador".

### 4 - Ouvir a História (Opcional): 
  + Se desejar, você pode ouvir a história gerada clicando no botão "Gerar Audio da História".
  + Após o áudio gerado clique em "Reproduzir História".

### 5 - Aceitar a História: 
  + Se estiver satisfeito com a história gerada, clique no botão "Aceitar a história".
  + Isso salvará a história atual e limpará a caixa de texto de entrada para a próxima etapa.

### 6 - Continuar a História (Opcional): 
  + Você pode continuar adicionando detalhes à história, seja falando ou digitando na caixa de texto, e repetindo os passos 2 a 5.
  + Isso permite que você colabore com a IA para expandir a história em várias etapas.

### 7 - Gerar Saídas Finais:
  + Quando estiver satisfeito com a história completa, você pode gerá-la em diferentes formatos:
    * Clique em "Gerar PDF" para gerar um arquivo PDF da sua história.
    * Clique em "Gerar Áudio" para gerar um arquivo de áudio da sua história.

### 8 - Baixar Arquivos: 
  + Os arquivos PDF e de áudio gerados estarão disponíveis para download.
  + Basta clicar nos links fornecidos para baixar os arquivos para o seu dispositivo.
