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
        
        # Exibe a imagem apenas uma vez aqui
        st.image(image, caption='Imagem do cartão de crédito', use_container_width=True)
        
        # Enviar para o blob e pegar a url
        blob_url = upload_blob(image, fileName)
        if blob_url:
            st.write(f"O arquivo {fileName} foi enviado com sucesso!")
            
            with st.spinner("Analisando informações do cartão..."):
                credit_card_info = analyze_credit_card(blob_url)
                
            if credit_card_info:
                show_credit_card_info(credit_card_info)
            else:
                st.error("Não foi possível analisar as informações do cartão. Verifique se a imagem é clara e contém um cartão de crédito válido.")

def show_credit_card_info(credit_card_info):
    st.subheader("Informações do Cartão de Crédito")
    
    # Verifica se alguma informação relevante foi detectada
    has_info = any([
        credit_card_info.get("card_name", ""),
        credit_card_info.get("card_number", ""),
        credit_card_info.get("card_expiration", ""),
        credit_card_info.get("bank_name", "")
    ])
    
    if has_info:
        st.success("Informações detectadas!")
        
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Nome no cartão:**")
            st.write("**Rede de pagamento:**")
            st.write("**Número do cartão:**")
            st.write("**Data de expiração:**")
        
        with col2:
            st.write(f"{credit_card_info.get('card_name') or 'Não detectado'}")
            st.write(f"{credit_card_info.get('bank_name') or 'Não detectado'}")
            st.write(f"{credit_card_info.get('card_number') or 'Não detectado'}")
            st.write(f"{credit_card_info.get('card_expiration') or 'Não detectado'}")
    else:
        st.warning("Nenhuma informação do cartão foi detectada.")
        
    # Mostre os dados brutos (pode ser removido na versão final)
    with st.expander("Ver dados brutos"):
        st.json(credit_card_info)

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