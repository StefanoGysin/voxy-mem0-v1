"""
Aplicação Streamlit para o Voxy-Mem0.
"""
import streamlit as st
from utils.session import initialize_session
from components.sidebar import render_sidebar

# Configuração da página
st.set_page_config(
    page_title="Voxy-Mem0 - Assistente com Memória",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa a sessão
initialize_session()

# Título principal
st.title("🧠 Voxy-Mem0")
st.subheader("Assistente com Memória Vetorial")

# Renderiza a barra lateral
render_sidebar()

# Conteúdo principal
st.write("""
Bem-vindo ao Voxy-Mem0, um assistente conversacional com memória vetorial de longo prazo.
Este assistente lembra de conversas anteriores e fornece respostas contextualizadas.

### Como usar:
1. Digite seu ID de usuário na barra lateral (ou use o ID gerado automaticamente)
2. Inicie uma conversa na página de Chat
3. O assistente lembrará de informações anteriores durante a conversa

### Recursos:
- 🧠 Memória vetorial persistente
- 👤 Suporte a múltiplos usuários
- 💬 Respostas contextuais
""")

# Botão para ir para o chat
if st.button("Iniciar Chat", type="primary"):
    st.switch_page("pages/chat.py")
