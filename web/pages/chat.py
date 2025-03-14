"""
Página de chat do Voxy-Mem0.
"""
import streamlit as st
from utils.session import initialize_session, add_message, get_messages
from utils.api import process_message
from components.sidebar import render_sidebar

# Configuração da página
st.set_page_config(
    page_title="Chat - Voxy-Mem0",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa a sessão
initialize_session()

# Renderiza a barra lateral
render_sidebar()

# Título da página
st.title("💬 Chat com Voxy-Mem0")

# Exibe o histórico de mensagens
for message in get_messages():
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Campo de entrada para nova mensagem
if prompt := st.chat_input("Digite sua mensagem..."):
    # Adiciona a mensagem do usuário ao histórico
    add_message("user", prompt)

    # Exibe a mensagem do usuário
    with st.chat_message("user"):
        st.write(prompt)

    # Processa a mensagem e obtém a resposta
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            user_id = st.session_state.user_id
            response = process_message(prompt, user_id)
            st.write(response)

    # Adiciona a resposta do assistente ao histórico
    add_message("assistant", response)

# Botões de controle
col1, col2 = st.columns(2)
with col1:
    if st.button("Limpar Chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

with col2:
    if st.button("Nova Conversa", type="primary"):
        st.session_state.messages = []
        st.rerun()
