import streamlit as st
import os
from google import genai

# Configuración de página
st.set_page_config(page_title="Decoy Troy – Community Insider", layout="wide")
st.title("Decoy Troy – Real Estate Marketing Engine")

# Credenciales de Railway
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Configuración faltante: Agrega GOOGLE_API_KEY en Railway.")
    st.stop()

# Inicializar el nuevo cliente
client = genai.Client(api_key=api_key)

# Tus instrucciones de sistema (simplificado para el ejemplo)
system_instruction = "Eres Decoy Troy... (Aquí va todo tu texto largo)"

# IDs de tus archivos
PERMANENT_KNOWLEDGE_BASE_IDS = ["files/rrzx4s5xok9q", "files/7138egrcd187", "files/t1nw56cbxekp"]

# Gestión de historial
if "messages" not in st.session_state:
    st.session_state.messages = []

# Sidebar
with st.sidebar:
    st.header("🕵️ Decoy Troy's Intel")
    st.success(f"✅ {len(PERMANENT_KNOWLEDGE_BASE_IDS)} Intel Documents Active.")

# Mostrar historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- LÓGICA DE CHAT CORREGIDA ---
if prompt := st.chat_input("Enter City, Zip Code, or Neighborhood..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        # En la nueva librería, así se envía el mensaje con contexto y archivos:
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            config={
                'system_instruction': system_instruction,
            },
            contents=[prompt] + PERMANENT_KNOWLEDGE_BASE_IDS
        )
        
        text_response = response.text
        
        with st.chat_message("assistant"):
            st.markdown(text_response)
        
        st.session_state.messages.append({"role": "assistant", "content": text_response})
        
    except Exception as e:
        st.error(f"Error: {e}")
