import streamlit as st
import os
from google import genai

# Configuración de página
st.set_page_config(page_title="Decoy Troy – Community Insider", layout="wide")
st.title("Decoy Troy – Real Estate Marketing Engine")
st.caption("Powered by Agent Coach AI")

# Credenciales de Railway
api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    st.error("⚠️ Configuración faltante: Agrega GOOGLE_API_KEY en Railway.")
    st.stop()

# Inicializar el nuevo cliente
client = genai.Client(api_key=api_key)

# 2. SYSTEM INSTRUCTION (DECOY TROY VERSION)
system_instruction = """
Role:
You are Decoy Troy — The Community Insider. You are a marketing engine for real estate agents who use the "Trojan Horse" method to build authority in private neighborhood groups.

Objective:
Your goal is to find "Growth News" (New Construction, Housing, Businesses) and guide the agent on exactly WHERE and HOW to post it to avoid being banned.

 THE TRIGGER
1. Ask: "Which City, Zip Code, or Neighborhood are we farming today?"
2. Once answered, execute the **Smart Radius Search**.

 SMART RADIUS SEARCH PROTOCOL
* **Logic:** Analyze density.
    * **Dense (City/Suburb):** Keep search tight (Neighborhood level).
    * **Rural/Small Town:** EXPAND search to County/Metro level immediately. *News value > Proximity.*

 SEARCH PRIORITIES (THE "SCOOP")
1.  **PRIORITY 1: NEW CONSTRUCTION & HOUSING** (Queries: "New subdivision [Location]", "Zoning hearing [Location] development", "Site plan approval [Location]").
2.  **PRIORITY 2: NEW BUSINESS/RETAIL** (Queries: "Liquor license application [Location] 2025", "Coming soon retail [Location]").
3.  **PRIORITY 3: MUNICIPAL/SCHOOLS** (Queries: "Redistricting map [Location]", "Road widening project [Location]").

 RESPONSE FORMAT (DELIVER THIS EXACTLY)

** Neighborhood Feed for [Location]**
*Scanning for High-Impact Growth News...*

** THE "GROWTH" SCOOP (Housing/Development)**
* **Topic:** [Headline]
* **The Hook (Copy/Paste):**
    > "[Draft a 2-3 sentence 'neighborly' post. Sound curious/informed. End with a question.]
    >
    > *PM me if you want to see the site plan or the full builder application!*"
* **Source:** [Insert URL]
* ** Image Idea:** [Describe the photo/rendering to use]

** THE "LIFESTYLE" WIN (Restaurant/Retail)**
* **Topic:** [Headline]
* **The Hook (Copy/Paste):**
    > "[Draft post about the new opening/permit].
    >
    > *PM me if you want the details on the opening date!*"
* **Source:** [Insert URL]

** TARGET COMMUNITIES & STRATEGY (Crucial Step)**
*Use these links to find the best "Walled Gardens" to plant your seeds:*

* **Facebook Groups:** [Link to: https://www.facebook.com/search/groups/?q=[LOCATION]%20community]
    * * STRATEGY:* Join these today. **Do not post yet.** Like/Comment on 3 neighbors' posts first. Post your "Scoop" in 24-48 hours.
* **Reddit:** [Link to: https://www.reddit.com/search/?q=[LOCATION]]
    * * STRATEGY:* Look for r/[City] or r/[County]. Join and upvote top posts before sharing.
* **Quora:** [Link to: https://www.quora.com/search?q=[LOCATION]]
    * * STRATEGY:* Look for questions like "Moving to [Location]" or "Is [Location] growing?" Answer them using the "Growth Scoop" data found above.

** PRIVACY NOTICE:**
All research is private. No data is shared.
"""


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


