from dataclasses import dataclass, field
from typing import Dict, List
import streamlit as st
from datetime import datetime

@dataclass
class ChatState:
    chat_id: str
    messages: List[Dict] = field(default_factory=list)
    summary: Dict = field(default_factory=dict)
    files: List[Dict] = field(default_factory=list)

def generate_chat_id() -> str:
    return f'chat_{datetime.now().strftime("%Y%m%d_%H%M%S")}'

def get_chat_state(chat_id: str = None) -> ChatState:
    if not chat_id:
        chat_id = generate_chat_id()
    
    if chat_id not in st.session_state:
        st.session_state[chat_id] = ChatState(chat_id=chat_id)
    
    return st.session_state[chat_id]

def get_all_chats() -> List[str]:
    return [k for k in st.session_state.keys() if k.startswith('chat_')]

def clear_chat_state(chat_id: str) -> None:
    if chat_id in st.session_state:
        del st.session_state[chat_id]