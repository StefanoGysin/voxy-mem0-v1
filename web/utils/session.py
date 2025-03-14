"""
Utilitários para gerenciamento de sessão no Streamlit.
"""
import streamlit as st
from datetime import datetime
import uuid

def initialize_session():
    """
    Inicializa a sessão do Streamlit com valores padrão.
    """
    if "user_id" not in st.session_state:
        st.session_state.user_id = "web_user_" + str(uuid.uuid4())[:8]

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "session_start" not in st.session_state:
        st.session_state.session_start = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def set_user_id(user_id: str):
    """
    Define o ID do usuário para a sessão atual.

    Args:
        user_id: ID do usuário
    """
    if user_id and user_id.strip():
        st.session_state.user_id = user_id.strip()
        # Limpa as mensagens ao trocar de usuário
        st.session_state.messages = []

def get_user_id() -> str:
    """
    Obtém o ID do usuário da sessão atual.

    Returns:
        str: ID do usuário
    """
    return st.session_state.user_id

def add_message(role: str, content: str):
    """
    Adiciona uma mensagem ao histórico da sessão.

    Args:
        role: Papel do emissor ('user' ou 'assistant')
        content: Conteúdo da mensagem
    """
    st.session_state.messages.append({"role": role, "content": content})

def get_messages():
    """
    Obtém todas as mensagens da sessão atual.

    Returns:
        list: Lista de mensagens
    """
    return st.session_state.messages

def clear_messages():
    """
    Limpa todas as mensagens da sessão atual.
    """
    st.session_state.messages = []
