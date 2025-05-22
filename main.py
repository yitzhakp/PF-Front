import streamlit as st
import requests
#import openai  # o llama tu LLM local

# Opcional: configura tu clave si usas OpenAI
#openai.api_key = st.secrets.get("openai_api_key", "")

# URL de tu API para diagnóstico EEG
API_URL = "https://upset-sheila-kathryn-yitzhakp-e72da9a3.koyeb.app/predict_from_set"

# Función para enviar archivo a la API
def obtener_diagnostico_desde_api(archivo):
    
    archivos = {'file': archivo}
    respuesta = requests.post(API_URL, files=archivos)
    
    if respuesta.status_code == 200:
        return respuesta.json()  # Ejemplo: {"probabilidad": 0.82}
    else:
        st.error("Error al consultar la API")
        return None

# Función para generar respuesta con LLM
def generar_respuesta_llm(probabilidad):
    prompt = f"""
Eres un asistente empático que ayuda a familiares de pacientes con Alzheimer.
Un modelo de IA ha analizado un EEG y ha estimado una probabilidad de {probabilidad*100:.1f}% de que la persona tenga Alzheimer.
Explica con empatía qué significa este resultado y qué pasos podrían seguir.
"""
    return "Hola cuidate"
    respuesta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # O reemplaza por tu LLM local
        messages=[{"role": "user", "content": prompt}]
    )
    return respuesta.choices[0].message.content

# Interfaz Streamlit
st.title("Asistente de Alzheimer con IA + EEG")

archivo_eeg = st.file_uploader("Sube un archivo EEG (.set)", type=["set"])

if archivo_eeg is not None:
    with st.spinner("Analizando el archivo EEG..."):
        resultado = obtener_diagnostico_desde_api(archivo_eeg)
        if resultado:
            prob = resultado.get("mean probability", 0.0)
            st.success(f"Probabilidad estimada de Alzheimer: {prob*100:.1f}%")
            
            with st.spinner("Generando respuesta personalizada..."):
                respuesta = generar_respuesta_llm(prob)
                st.markdown("### Respuesta del asistente:")
                st.markdown(respuesta)
