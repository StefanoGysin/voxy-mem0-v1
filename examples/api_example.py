#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Exemplo de uso programático da API do Voxy-Mem0.
Este script demonstra como usar o agente Voxy-Mem0 em outras aplicações.
"""

import os
import sys
import logging
from dotenv import load_dotenv

# Adiciona o diretório pai ao path para importar o módulo voxy_agent
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(parent_dir)

# Importa as funções do módulo voxy_agent
from voxy_agent import setup_memory, chat_with_memories, __version__

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("voxy-api-example")

def demonstrate_api_usage():
    """Demonstra como usar a API do Voxy-Mem0 programaticamente"""
    
    print(f"Voxy-Mem0 API Example v{__version__}")
    print("=" * 50)
    
    # Carrega variáveis de ambiente
    load_dotenv()
    
    try:
        # Inicializa os componentes
        print("Inicializando agente...")
        openai_client, memory = setup_memory()
        
        # Define um ID de usuário para teste
        user_id = "exemplo_api"
        
        # Função de exemplo para processar mensagens
        def process_message(message):
            logger.info(f"Processando mensagem: {message}")
            
            response = chat_with_memories(
                message=message,
                user_id=user_id,
                openai_client=openai_client,
                memory=memory
            )
            
            return response
        
        # Exemplos de uso
        print("\nExemplo 1: Perguntas simples")
        print("-" * 50)
        
        questions = [
            "Meu nome é Maria Silva.",
            "Eu trabalho como engenheira de software.",
            "Quem sou eu?"
        ]
        
        for question in questions:
            print(f"\nPergunta: {question}")
            answer = process_message(question)
            print(f"Resposta: {answer}")
        
        print("\nExemplo 2: Uso em loop de aplicação")
        print("-" * 50)
        print("Este padrão pode ser usado em aplicações web, chatbots, etc.")
        
        print("""
# Exemplo de uso em uma aplicação:
        
def handle_user_message(user_message, user_identifier):
    response = chat_with_memories(
        message=user_message,
        user_id=user_identifier,
        openai_client=openai_client,
        memory=memory
    )
    return response
    
# Em uma aplicação web (exemplo Flask):
@app.route('/chat', methods=['POST'])
def chat_endpoint():
    data = request.json
    user_message = data.get('message')
    user_id = data.get('user_id', 'web_user')
    
    response = handle_user_message(user_message, user_id)
    
    return jsonify({
        'response': response,
        'user_id': user_id
    })
""")
        
        print("\nExemplo completo concluído com sucesso!")
        
    except Exception as e:
        logger.error(f"Erro na demonstração: {str(e)}")
        print(f"Ocorreu um erro: {str(e)}")
        print("Verifique se suas variáveis de ambiente estão configuradas corretamente.")

if __name__ == "__main__":
    demonstrate_api_usage() 