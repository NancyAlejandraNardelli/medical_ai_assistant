import streamlit as st
from app.components.sidebar import render_sidebar
from app.components.chat_window import render_chat_window
from app.components.summary_tab import render_summary_tab
from app.components.file_list import render_file_list
from app.utils.session_state import generate_chat_id

# Configuración de la página
st.set_page_config(
    page_title="Medical AI Assistant",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos personalizados
st.markdown("""
<style>
    .main > div {
        padding: 2rem 3rem;
        max-width: 1100px;
    }
    .stButton button {
        border-radius: 1rem;
        padding: 0.5rem 1rem;
    }
    .stChatMessage {
        background-color: #ffffff;
        border-radius: 1rem;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Inicializar el chat_id actual si no existe
if 'current_chat_id' not in st.session_state:
    st.session_state['current_chat_id'] = generate_chat_id()

# Renderizar sidebar
render_sidebar(st.session_state['current_chat_id'])

# Contenido principal
tab1, tab2, tab3 = st.tabs(['💬 Chat', '📋 Resumen', '📎 Archivos'])

with tab1:
    render_chat_window(st.session_state['current_chat_id'])

with tab2:
    render_summary_tab(st.session_state['current_chat_id'])

with tab3:
    render_file_list(st.session_state['current_chat_id'])