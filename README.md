## 📋 Descrição do Projeto

O Credit Card Reader é uma aplicação que permite fazer upload de imagens de cartões de crédito e extrair automaticamente as informações contidas neles, como número do cartão, nome do titular, data de expiração e banco emissor.

## 🚀 Funcionalidades

- Interface web amigável para upload de imagens
- Suporte para formatos JPG, PNG e JPEG
- Análise automática de cartões de crédito
- Extração de informações importantes:
  - Nome do titular
  - Número do cartão
  - Data de validade
  - Banco emissor
- Armazenamento seguro das imagens em Azure Blob Storage

## 💻 Tecnologias Utilizadas

- Python
- Streamlit (para interface web)
- Azure Storage Blob (para armazenamento de imagens)
- Computer Vision API (para análise das imagens)

## 🛠️ Instalação e Configuração

1. Clone o repositório:
```shell script
git clone https://github.com/seu-usuario/Credit_card_reader.git
cd Credit_card_reader
```


2. Crie e ative um ambiente virtual:
```shell script
python -m venv .venv
source .venv/bin/activate  # No Windows: .venv\Scripts\activate
```


3. Instale as dependências:
```shell script
pip install -r src/requirements.txt
```


4. Configure as variáveis de ambiente:
   - Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```
AZURE_STORAGE_CONNECTION_STRING=sua_connection_string
   CONTAINER_NAME=nome_do_container
```


## 🚀 Executando a Aplicação

Execute o aplicativo Streamlit com o comando:
```shell script
streamlit run src/app.py
```



## 🔒 Segurança

As informações dos cartões de crédito são processadas localmente e não são armazenadas permanentemente. As imagens são armazenadas no Azure Blob Storage para análise temporária.

## 📝 Nota Importante

Esta aplicação é apenas para fins de demonstração e uso pessoal. Não utilize para armazenar informações reais de cartões de crédito sem implementar as medidas de segurança adequadas.
