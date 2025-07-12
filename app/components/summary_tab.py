import streamlit as st
from ..services.api_client import api_client
from ..utils.session_state import get_chat_state

def render_patient_card(patient_data: dict):
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric('Edad', f"{patient_data.get('edad', 'N/A')} años")
        with col2:
            st.metric('Sexo', patient_data.get('sexo', 'N/A'))
        with col3:
            triage = patient_data.get('triage', 'N/A')
            st.metric('Triage', triage, delta_color='off')

def get_section_color(section_name: str) -> str:
    colors = {
        'Diagnóstico': '#FF6B6B',
        'Laboratorio': '#4ECDC4',
        'Tratamiento': '#45B7D1',
        'Antecedentes': '#96CEB4',
        'Examen Físico': '#FFEEAD'
    }
    return colors.get(section_name, '#147AFF')

def render_summary_tab(chat_id: str):
    chat_state = get_chat_state(chat_id)
    
    if not chat_state.summary:
        with st.spinner('Cargando resumen médico...'):
            summary_data = api_client.get_summary(chat_id)
            if summary_data:
                chat_state.summary = summary_data
    
    if chat_state.summary:
        st.subheader('📋 Resumen del Caso')
        
        # Datos del paciente
        if 'patient_data' in chat_state.summary:
            render_patient_card(chat_state.summary['patient_data'])
        
        st.markdown('---')
        
        # Secciones del resumen
        if 'sections' in chat_state.summary:
            for section_name, content in chat_state.summary['sections'].items():
                with st.expander(f"📑 {section_name}"):
                    st.markdown(
                        f'<div style="padding: 1rem; border-radius: 0.5rem; '
                        f'background-color: {get_section_color(section_name)}15;">{content}</div>',
                        unsafe_allow_html=True
                    )
    else:
        st.info('No hay resumen médico disponible para este caso.')