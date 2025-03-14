"""
Componente da barra lateral para a aplicação Streamlit.
"""
import streamlit as st
from utils.session import get_user_id, set_user_id

def render_sidebar():
    """
    Renderiza a barra lateral da aplicação.
    """
    with st.sidebar:
        st.image("https://github.com/mem0ai/mem0/raw/main/docs/public/logo.png", width=100)
        st.title("Voxy-Mem0")

        # Navegação
        st.subheader("Navegação")

        # Links para as páginas
        st.page_link("app.py", label="Início", icon="🏠")
        st.page_link("pages/chat.py", label="Chat", icon="💬")
        st.page_link("pages/about.py", label="Sobre", icon="ℹ️")
        st.page_link("pages/settings.py", label="Configurações", icon="⚙️")

        # Configuração do usuário
        st.subheader("Usuário")

        current_user_id = get_user_id()
        new_user_id = st.text_input(
            "ID do Usuário",
            value=current_user_id,
            help="Identificador único para suas memórias"
        )

        if st.button("Atualizar ID"):
            set_user_id(new_user_id)
            st.success(f"ID atualizado para: {new_user_id}")

        # Informações da sessão
        st.subheader("Informações")
        st.info(f"ID atual: {get_user_id()}")

        if "session_start" in st.session_state:
            st.info(f"Sessão iniciada: {st.session_state.session_start}")

        # Rodapé
        st.divider()
        st.caption("Voxy-Mem0 v1.0.0")
        st.caption("Powered by Mem0 & OpenAI")
