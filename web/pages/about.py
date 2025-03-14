"""
Página sobre o Voxy-Mem0.
"""
import streamlit as st
from components.sidebar import render_sidebar

# Configuração da página
st.set_page_config(
    page_title="Sobre - Voxy-Mem0",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Renderiza a barra lateral
render_sidebar()

# Título da página
st.title("ℹ️ Sobre o Voxy-Mem0")

# Conteúdo da página
st.write("""
## O que é o Voxy-Mem0?

Voxy-Mem0 é um assistente conversacional baseado em IA com memória vetorial de longo prazo.
Desenvolvido com a biblioteca [Mem0](https://github.com/mem0ai/mem0) e integrado com a API da OpenAI
e banco de dados Supabase, este assistente oferece uma experiência de conversação personalizada
ao lembrar conversas anteriores, preferências e informações contextuais dos usuários.

## Funcionalidades

- **🧠 Memória Vetorial Persistente**: Armazena e recupera conversas anteriores usando embeddings
- **👤 Identificação de Usuários**: Permite múltiplos usuários com memórias individuais
- **🔒 Armazenamento Seguro**: Dados armazenados de forma segura no Supabase com pgvector
- **💬 Respostas Contextuais**: Gera respostas levando em consideração o histórico da conversa
- **📝 Logging Detalhado**: Sistema de registro para monitoramento e depuração
- **🚀 Fácil de Usar**: Interface web simples e intuitiva

## Como Funciona

O Voxy-Mem0 utiliza um sistema de Retrieval-Augmented Generation (RAG):

1. Quando você envia uma mensagem, o sistema busca memórias relevantes no banco de dados
2. Essas memórias são usadas para contextualizar sua pergunta
3. O modelo de linguagem (LLM) gera uma resposta considerando esse contexto
4. A conversa é armazenada como uma nova memória para uso futuro

## Tecnologias Utilizadas

- **Frontend**: Streamlit
- **Backend**: Python
- **LLM**: OpenAI API (GPT-4o-mini)
- **Banco de Dados**: Supabase com pgvector
- **Biblioteca de Memória**: Mem0
""")

# Exibe o logo
st.image("https://github.com/mem0ai/mem0/raw/main/docs/public/logo.png", width=150)

# Informações adicionais
st.divider()
st.write("### Créditos")
st.write("Desenvolvido com ❤️ pela equipe Voxy")
st.write("Licença: MIT")
