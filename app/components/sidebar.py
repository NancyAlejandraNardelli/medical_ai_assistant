import streamlit as st
from ..services.api_client import api_client
from ..utils.session_state import get_all_chats, generate_chat_id, clear_chat_state

def render_sidebar(current_chat_id: str):
    with st.sidebar:
        st.title('🩺 Medical AI')
        st.markdown('---')

        # Botón New Chat
        if st.button('+ New Chat', use_container_width=True):
            new_chat_id = generate_chat_id()
            clear_chat_state(current_chat_id)
            st.session_state['current_chat_id'] = new_chat_id
            st.experimental_rerun()

        st.markdown('---')

        # Historial de chats
        st.subheader('Historial de Consultas')
        chat_list = get_all_chats()
        
        for chat_id in chat_list:
            if st.sidebar.button(
                f"📝 {chat_id.replace('chat_', 'Consulta ')}",
                key=f'btn_{chat_id}',
                use_container_width=True
            ):
                st.session_state['current_chat_id'] = chat_id
                st.experimental_rerun()

        st.markdown('---')

        # File uploader
        st.subheader('Subir Historia Clínica')
        uploaded_files = st.file_uploader(
            "Archivos (.docx, PDF)",
            accept_multiple_files=True,
            type=['docx', 'pdf']
        )

        if uploaded_files:
            for file in uploaded_files:
                with st.spinner(f'Subiendo {file.name}...'):
                    response = api_client.upload_file(current_chat_id, file)
                    if response.get('ok'):
                        st.success(f'{file.name} subido correctamente')
                    else:
                        st.error(f'Error al subir {file.name}')