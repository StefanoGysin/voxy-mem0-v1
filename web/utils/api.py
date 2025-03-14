"""
API wrapper para integrar o Streamlit com o núcleo do Voxy-Mem0.
"""
import sys
import os
from typing import Dict, List, Any

# Adiciona o diretório raiz ao path para importar o módulo voxy_agent
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Importa as funções do módulo voxy_agent
from voxy_agent import setup_memory, chat_with_memories

# Instâncias globais para reutilização
_openai_client = None
_memory = None

def initialize_api():
    """
    Inicializa a API do Voxy-Mem0.

    Returns:
        tuple: (openai_client, memory) - Clientes inicializados
    """
    global _openai_client, _memory

    if _openai_client is None or _memory is None:
        _openai_client, _memory = setup_memory()

    return _openai_client, _memory

def process_message(message: str, user_id: str) -> str:
    """
    Processa uma mensagem do usuário usando o Voxy-Mem0.

    Args:
        message: Mensagem do usuário
        user_id: ID do usuário

    Returns:
        str: Resposta do assistente
    """
    openai_client, memory = initialize_api()

    response = chat_with_memories(
        message=message,
        user_id=user_id,
        openai_client=openai_client,
        memory=memory
    )

    return response

def get_user_memories(user_id: str, limit: int = 10) -> List[Dict[str, Any]]:
    """
    Recupera as memórias de um usuário.

    Args:
        user_id: ID do usuário
        limit: Número máximo de memórias a retornar

    Returns:
        List[Dict]: Lista de memórias do usuário
    """
    _, memory = initialize_api()

    # Busca todas as memórias do usuário (query vazia)
    memories = memory.search(query="", user_id=user_id, limit=limit)

    return memories["results"]
