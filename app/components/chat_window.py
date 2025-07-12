import streamlit as st
from typing import List, Dict
from ..services.api_client import api_client
from ..utils.session_state import get_chat_state

def render_message(message: Dict):
    with st.chat_message(message['role']):
        st.markdown(message['content'])

def render_chat_window(chat_id: str):
    chat_state = get_chat_state(chat_id)
    
    # Renderizar mensajes existentes
    for message in chat_state.messages:
        render_message(message)
    
    # Input de chat
    if prompt := st.chat_input('Escribe tu pregunta aquí...'):
        # Agregar mensaje del usuario
        user_message = {'role': 'user', 'content': prompt}
        chat_state.messages.append(user_message)
        render_message(user_message)
        
        # Obtener respuesta del asistente
        with st.spinner('Pensando...'):
            response = api_client.chat(chat_id, prompt)
            
            if response and 'answer' in response:
                assistant_message = {
                    'role': 'assistant',
                    'content': response['answer']
                }
                chat_state.messages.append(assistant_message)
                render_message(assistant_message)
            else:
                st.error('No se pudo obtener una respuesta. Por favor, intenta de nuevo.')

def clear_chat():
    if 'messages' in st.session_state:
        st.session_state.messages = []