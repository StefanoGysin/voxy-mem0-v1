"""
Página de configurações do Voxy-Mem0.
"""
import streamlit as st
from utils.session import initialize_session, get_user_id, clear_messages
from utils.api import get_user_memories
from components.sidebar import render_sidebar

# Configuração da página
st.set_page_config(
    page_title="Configurações - Voxy-Mem0",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inicializa a sessão
initialize_session()

# Renderiza a barra lateral
render_sidebar()

# Título da página
st.title("⚙️ Configurações")

# Configurações do usuário
st.subheader("Configurações do Usuário")

user_id = get_user_id()
st.info(f"ID do usuário atual: {user_id}")

# Opções de configuração
st.subheader("Opções de Chat")

# Modelo de linguagem
model_options = ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"]
selected_model = st.selectbox(
    "Modelo de Linguagem",
    options=model_options,
    index=0,
    help="Selecione o modelo de linguagem a ser utilizado"
)

# Número de memórias a recuperar
memory_limit = st.slider(
    "Limite de Memórias",
    min_value=1,
    max_value=10,
    value=5,
    help="Número máximo de memórias a serem recuperadas por consulta"
)

# Botão para salvar configurações
if st.button("Salvar Configurações", type="primary"):
    # Aqui implementaríamos a lógica para salvar as configurações
    # Por enquanto, apenas mostramos uma mensagem de sucesso
    st.success("Configurações salvas com sucesso!")

# Gerenciamento de memórias
st.subheader("Gerenciamento de Memórias")

# Exibir memórias do usuário
if st.button("Mostrar Minhas Memórias"):
    with st.spinner("Carregando memórias..."):
        try:
            memories = get_user_memories(user_id)

            if memories:
                st.write(f"Encontradas {len(memories)} memórias para o usuário {user_id}:")

                for i, memory in enumerate(memories):
                    with st.expander(f"Memória {i+1}"):
                        st.json(memory)
            else:
                st.info("Nenhuma memória encontrada para este usuário.")
        except Exception as e:
            st.error(f"Erro ao carregar memórias: {str(e)}")

# Opções de limpeza
st.subheader("Limpar Dados")

col1, col2 = st.columns(2)

with col1:
    if st.button("Limpar Histórico de Chat", type="secondary"):
        clear_messages()
        st.success("Histórico de chat limpo com sucesso!")
        st.rerun()

with col2:
    if st.button("Limpar Todas as Memórias", type="secondary"):
        # Esta funcionalidade exigiria uma implementação adicional na API
        st.warning("Esta funcionalidade ainda não está implementada.")
