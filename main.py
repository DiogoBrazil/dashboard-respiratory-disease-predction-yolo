import streamlit as st
import numpy as np
from PIL import Image
import time
from ultralytics import YOLO
import matplotlib.pyplot as plt
import cv2

@st.cache_resource
def load_model():
    model = YOLO('models/best.pt') 
    return model

model = load_model()

def predict(image, model):
    return model(image)

def load_file_to_dictionary(file_path):
    result_dict = {}

    with open(file_path, 'r') as file:
        for line in file:
            value, disease = line.strip().split(' ', 1)
            result_dict[disease] = float(value) * 100  
    return result_dict

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

st.title("Detecção de doenças respiratórias")

uploaded_file = st.file_uploader("Escolha uma imagem de Raio-X que contenha a região pulmonar", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    
    st.image(image, caption='Imagem carregada', use_column_width=False, width=700)

    message_placeholder = st.empty()
    try:
        with st.spinner('Fazendo previsão...'):
            time.sleep(2)
            predictions = predict(image, model)
            predictions[0].save_txt('results.txt')
            result_dict = load_file_to_dictionary('results.txt')
            message_placeholder.success("Previsão feita com sucesso")
            time.sleep(2)
            message_placeholder.empty()
            
            plot_predictions(result_dict)
    except Exception as e:
        message_placeholder.error("Erro ao fazer a previsão")
        time.sleep(2)
        message_placeholder.empty()
