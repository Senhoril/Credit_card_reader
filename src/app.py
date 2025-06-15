import os
import sys
from azure.storage.blob import BlobServiceClient
import streamlit as st

# Adiciona a pasta raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.utils.Config import Config
from src.services.credit_card_service import analyze_credit_card

def configure_interface():
    st.title("Upload credit card")
    uploaded_file = st.file_uploader("Choose a file", type=["jpg","png","jpeg"])
    if uploaded_file is not None:
        image = uploaded_file.read()
        fileName = uploaded_file.name
        st.write("Filename:", fileName)
        
        # Exibe a imagem apenas uma vez
        st.image(image, caption='Imagem do cartão de crédito', use_container_width=True)
        
        # Enviar para o blob e pegar a url
        blob_url = upload_blob(image, fileName)
        if blob_url:
            st.write(f"O arquivo {fileName} foi enviado com sucesso!")
            
            with st.spinner("Analisando informações do cartão..."):
                credit_card_info = analyze_credit_card(blob_url)
            
            # Mostrar as informações do cartão
            show_credit_card_info(credit_card_info)

def show_credit_card_info(credit_card_info):
    st.write(f"O resultado da detecção de cartão de crédito é: {credit_card_info}")
    
    if credit_card_info and credit_card_info.get("card_name"):
        st.write(f"O nome do cartão de crédito é: {credit_card_info.get('card_name')}")
        st.write(f"Banco emissor: {credit_card_info.get('bank_name')}")
        st.write(f"O número do cartão de crédito é: {credit_card_info.get('card_number')}")
        st.write(f"Data de expiração do cartão de crédito é: {credit_card_info.get('card_expiration')}")
        
        # Não temos o CVV nas informações retornadas, então não vamos tentar exibi-lo
        # Isso evita o erro de chave
    else:
        st.warning("Não foi possível extrair informações completas do cartão de crédito.")

def upload_blob(file, file_name):
    try:
        blob_service_client = BlobServiceClient.from_connection_string(Config.AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(Config.CONTAINER_NAME)
        blob_client = container_client.get_blob_client(file_name)
        blob_client.upload_blob(file, overwrite=True)
        return blob_client.url
    except Exception as e:
        st.error(f"Erro ao enviar o arquivo para o blob: {e}")
        return None

if __name__ == "__main__":
    configure_interface()