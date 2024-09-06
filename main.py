import streamlit as st
from PIL import Image
import requests
import matplotlib.pyplot as plt
import io
import time

# Função para fazer a requisição à API
def predict_via_api(image):
    # Verifica o formato da imagem e ajusta o tipo MIME e extensão corretamente
    image_format = image.format.upper()
    
    if image_format == "JPG":
        image_format = "JPEG"  # Trata "JPG" como "JPEG"
    
    mime_type = f"image/{image_format.lower()}"  # Define o tipo MIME

    # Converte a imagem para bytes no formato correto (JPEG ou PNG)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image_format)
    img_byte_arr = img_byte_arr.getvalue()
    response = requests.post(
        f"{st.secrets['API_BASE_URL']}/predict",  # Substitua pelo URL da API
        files={"file": (f"image.{image_format.lower()}", img_byte_arr, mime_type)}  # Nome, conteúdo, tipo MIME
    )
    
    # Verifica a resposta
    if response.status_code == 200:
        return response.json()["prediction"]
    else:
        st.error(f"Erro na API: {response.status_code}")
        return None

# Função para plotar as previsões
def plot_predictions(predictions_dict):
    diseases = list(predictions_dict.keys())
    percentages = list(predictions_dict.values())
    
    colors = ['blue', 'green', 'red', 'orange']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(diseases, percentages, color=colors)
    
    ax.set_ylabel('Probabilidade (%)')
    ax.set_title('Previsão de Doenças Respiratórias')

    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 1, f'{yval:.2f}%', ha='center', va='bottom')

    ax.set_xticks(range(len(diseases)))
    ax.set_xticklabels(diseases, rotation=15, ha='right')  
    plt.ylim(0, 110) 
    
    plt.tight_layout()

    st.pyplot(fig)

# Título da aplicação
st.title("Detecção de doenças respiratórias")

# Upload do arquivo de imagem
uploaded_file = st.file_uploader("Escolha uma imagem de Raio-X que contenha a região pulmonar", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.image(image, caption='Imagem carregada', use_column_width=False, width=700)

    message_placeholder = st.empty()

    try:
        # Faz a previsão chamando a API
        with st.spinner('Fazendo previsão...'):
            predictions = predict_via_api(image)
        
        if predictions:
            message_placeholder.success("Previsão feita com sucesso")
            time.sleep(2)
            message_placeholder.empty()
            plot_predictions(predictions)
        else:
            message_placeholder.error("Falha ao obter previsão")
            time.sleep(2)
            message_placeholder.empty()
    except Exception as e:
        st.error(f"Erro ao fazer a previsão: {e}")
