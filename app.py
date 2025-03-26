import streamlit as st
import requests

# Configuración de Azure Computer Vision
AZURE_ENDPOINT = "https://visionisaaciad.cognitiveservices.azure.com/"
AZURE_KEY = st.secrets["AZURE_KEY"]
OCR_URL = f"{AZURE_ENDPOINT}vision/v3.2/ocr"

# Función para extraer la matrícula
def extract_license_plate(image_file):
    headers = {
        'Ocp-Apim-Subscription-Key': AZURE_KEY,
        'Content-Type': 'application/octet-stream'
    }
    
    response = requests.post(OCR_URL, headers=headers, data=image_file)
    response_data = response.json()
    
    license_plate = ""
    for region in response_data.get("regions", []):
        for line in region["lines"]:
            license_plate += " ".join([word["text"] for word in line["words"]]) + " "
    
    return license_plate.strip()

# Interfaz en Streamlit
st.title("Detección de Matrículas con Azure OCR")
uploaded_file = st.file_uploader("Sube una imagen de un vehículo", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption="Imagen subida", use_column_width=True)
    
    # Procesar imagen con OCR
    matricula_detectada = extract_license_plate(uploaded_file)
    
    if matricula_detectada:
        st.success(f"Matrícula detectada: {matricula_detectada}")
    else:
        st.error("No se detectó ninguna matrícula.")
