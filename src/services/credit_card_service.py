from azure.core.credentials import AzureKeyCredential
from azure.ai.documentintelligence import DocumentIntelligenceClient
from azure.ai.documentintelligence.models import AnalyzeDocumentRequest
import sys
import os
import streamlit as st

# Adiciona a pasta raiz do projeto ao path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.utils.Config import Config

def analyze_credit_card(card_url):
    try:
        credential = AzureKeyCredential(Config.KEY)
        document_client = DocumentIntelligenceClient(Config.ENDPOINT, credential)
        
        with st.spinner("Analisando cartão de crédito..."):
            card_info = document_client.begin_analyze_document("prebuilt-creditCard", AnalyzeDocumentRequest(url_source=card_url))
            result = card_info.result()
        
        if not result.documents:
            st.error("Nenhum documento foi retornado pela API.")
            return {"card_name": "", "card_number": "", "card_expiration": "", "bank_name": ""}
        
        for document in result.documents:
            fields = document.get("fields", {})
            
            # Mostra campos disponíveis (apenas para debug)
            st.write(f"Campos disponíveis: {list(fields.keys())}")
            
            # Extrai os valores corretos baseado nos nomes exatos dos campos
            card_holder_obj = fields.get("CardHolderName", {})
            card_number_obj = fields.get("CardNumber", {})
            expiration_date_obj = fields.get("ExpirationDate", {})
            payment_network_obj = fields.get("PaymentNetwork", {})
            
            # Tenta extrair os valores de cada objeto de diferentes maneiras
            card_name = ""
            if card_holder_obj:
                # Tenta obter o valor de diferentes propriedades possíveis
                card_name = (card_holder_obj.get("content", "") or 
                            card_holder_obj.get("value", "") or 
                            card_holder_obj.get("text", ""))
            
            card_number = ""
            if card_number_obj:
                card_number = (card_number_obj.get("content", "") or 
                              card_number_obj.get("value", "") or 
                              card_number_obj.get("text", ""))
            
            card_expiration = ""
            if expiration_date_obj:
                card_expiration = (expiration_date_obj.get("content", "") or 
                                  expiration_date_obj.get("value", "") or 
                                  expiration_date_obj.get("text", ""))
            
            # Usamos o PaymentNetwork como o "banco emissor" já que IssuingBank não está disponível
            bank_name = ""
            if payment_network_obj:
                bank_name = (payment_network_obj.get("content", "") or 
                            payment_network_obj.get("value", "") or 
                            payment_network_obj.get("text", ""))
            
            # Para debug, mostra a estrutura completa dos objetos
            st.write("Detalhes dos campos:")
            st.write(f"CardHolderName: {card_holder_obj}")
            st.write(f"CardNumber: {card_number_obj}")
            st.write(f"ExpirationDate: {expiration_date_obj}")
            st.write(f"PaymentNetwork: {payment_network_obj}")
            
            return {
                "card_name": card_name,
                "card_number": card_number,
                "card_expiration": card_expiration,
                "bank_name": bank_name  # Na verdade, este é o PaymentNetwork
            }
        
        return {"card_name": "", "card_number": "", "card_expiration": "", "bank_name": ""}
    
    except Exception as e:
        st.error(f"Erro ao analisar o cartão de crédito: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return {"card_name": "", "card_number": "", "card_expiration": "", "bank_name": ""}