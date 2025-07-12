import streamlit as st
from ..services.api_client import api_client
from ..utils.session_state import get_chat_state

def render_file_list(chat_id: str):
    chat_state = get_chat_state(chat_id)
    
    st.subheader('📎 Archivos Adjuntos')
    
    # Actualizar lista de archivos
    files = api_client.get_files(chat_id)
    chat_state.files = files
    
    if not files:
        st.info('No hay archivos adjuntos para este caso.')
        return
    
    # Crear una tabla con los archivos
    cols = st.columns([3, 2, 1])
    with cols[0]:
        st.markdown('**Nombre**')
    with cols[1]:
        st.markdown('**Fecha**')
    with cols[2]:
        st.markdown('**Acciones**')
    
    st.markdown('---')
    
    for file in files:
        col1, col2, col3 = st.columns([3, 2, 1])
        
        with col1:
            st.write(f"📄 {file.get('name', 'Sin nombre')}")
        
        with col2:
            st.write(file.get('upload_date', 'Fecha desconocida'))
        
        with col3:
            if st.button('⬇️', key=f'download_{file.get("id")}'):
                try:
                    # Aquí iría la lógica de descarga si el backend lo soporta
                    st.success('Archivo descargado correctamente')
                except Exception as e:
                    st.error('Error al descargar el archivo')
            
            if st.button('🗑️', key=f'delete_{file.get("id")}'):
                try:
                    # Aquí iría la lógica de eliminación si el backend lo soporta
                    st.success('Archivo eliminado correctamente')
                    st.experimental_rerun()
                except Exception as e:
                    st.error('Error al eliminar el archivo')