from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
import os
import logging
import sys
from datetime import datetime

# Informações da versão
__version__ = "1.0.0"
__author__ = "Voxy Team"

# Configuração de logging
log_path = os.path.join("logs", "voxy_agent.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(log_path)
    ]
)
logger = logging.getLogger("voxy-agent")

# Carrega variáveis de ambiente
load_dotenv()

# Banner do aplicativo
def display_banner():
    """Exibe o banner do aplicativo"""
    banner = f"""
    ╔═══════════════════════════════════════════════╗
    ║                 VOXY-MEM0                     ║
    ║     Assistente com Memória Vetorial v{__version__}     ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)
    print("  💭 Suas conversas com memória persistente")
    print("  🔒 Armazenamento seguro com Supabase")
    print("  🧠 Powered by Mem0 & OpenAI\n")

# Configuração do agente com memória
def setup_memory():
    """
    Configura e inicializa a camada de memória.
    Utiliza variáveis de ambiente para configuração.
    
    Returns:
        tuple: (openai_client, memory) - Clientes inicializados
        
    Raises:
        ValueError: Se as variáveis de ambiente necessárias não estiverem configuradas
        Exception: Para outros erros de configuração
    """
    logger.info("Inicializando configuração da memória")
    
    # Verifica configurações necessárias
    if not os.environ.get('DATABASE_URL'):
        logger.error("ERRO: DATABASE_URL não está configurado no arquivo .env!")
        logger.error("Por favor, configure as variáveis de ambiente conforme o .env.example")
        raise ValueError("DATABASE_URL não configurado")
            
    if not os.environ.get('OPENAI_API_KEY'):
        logger.error("ERRO: OPENAI_API_KEY não está configurado no arquivo .env!")
        logger.error("Por favor, configure as variáveis de ambiente conforme o .env.example")
        raise ValueError("OPENAI_API_KEY não configurado")
    
    # Configuração do agente com memória
    config = {
        "llm": {
            "provider": "openai",
            "config": {
                "model": os.getenv('MODEL_CHOICE', 'gpt-4o-mini')
            }
        },
        "vector_store": {
            "provider": "supabase",
            "config": {
                "connection_string": os.environ.get('DATABASE_URL'),
                "collection_name": "voxy_memories"
            }
        }    
    }
    
    try:
        openai_client = OpenAI()
        memory = Memory.from_config(config)
        logger.info("Configuração da memória concluída com sucesso")
        return openai_client, memory
    except Exception as e:
        logger.error(f"Erro ao configurar memória: {str(e)}")
        
        # Verificações específicas para erros comuns
        error_str = str(e)
        if "401" in error_str and "OpenAI" in error_str:
            logger.error("Erro de autenticação com a OpenAI. Verifique sua chave de API.")
        elif "supabase" in error_str.lower() or "database" in error_str.lower() or "db" in error_str.lower():
            logger.error("Erro de conexão com o Supabase. Verifique a URL de conexão.")
            logger.error("Dica: Execute 'python utils/setup_supabase.py' para diagnosticar problemas de conexão.")
        
        raise

def chat_with_memories(message: str, user_id: str = "default_user", openai_client=None, memory=None) -> str:
    """
    Processa uma mensagem do usuário usando a camada de memória.
    
    Args:
        message: Mensagem do usuário
        user_id: Identificador do usuário para personalização
        openai_client: Cliente da OpenAI
        memory: Instância da camada de memória
        
    Returns:
        str: Resposta do assistente baseada na memória
    """
    logger.info(f"Processando mensagem para usuário: {user_id}")
    
    try:
        # Recupera memórias relevantes
        relevant_memories = memory.search(query=message, user_id=user_id, limit=5)
        memories_str = "\n".join(f"- {entry['memory']}" for entry in relevant_memories["results"])
        
        logger.info(f"Recuperadas {len(relevant_memories['results'])} memórias relevantes")
        
        # Gera resposta do assistente
        system_prompt = (
            "Você é um assistente útil e amigável da Voxy. "
            "Responda à pergunta do usuário com base nas memórias disponíveis e na consulta atual.\n"
            f"Memórias do Usuário:\n{memories_str}"
        )
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": message}
        ]
        
        # Chamada para API da OpenAI com tratamento de erro melhorado
        try:
            response = openai_client.chat.completions.create(
                model=os.getenv('MODEL_CHOICE', 'gpt-4o-mini'),
                messages=messages
            )
            assistant_response = response.choices[0].message.content
        except Exception as api_error:
            logger.error(f"Erro na API OpenAI: {str(api_error)}")
            return f"Erro na comunicação com a OpenAI: {str(api_error)}"
        
        # Cria novas memórias a partir da conversa
        messages.append({"role": "assistant", "content": assistant_response})
        
        # Conta as memórias existentes antes de adicionar novas
        try:
            existing_memories_count = len(memory.search(query="", user_id=user_id, limit=100)["results"])
        except Exception as search_error:
            logger.warning(f"Erro ao contar memórias existentes: {str(search_error)}")
            existing_memories_count = 0
            
        # Adiciona a nova memória
        try:
            add_result = memory.add(messages, user_id=user_id)
        except Exception as add_error:
            logger.error(f"Erro ao adicionar memória: {str(add_error)}")
            print(f"\n⚠️ AVISO: Falha ao salvar memória: {str(add_error)}")
        
        # Verifica se novas memórias foram adicionadas
        try:
            new_memories_count = len(memory.search(query="", user_id=user_id, limit=100)["results"])
            new_memories_added = new_memories_count > existing_memories_count
        except Exception as verify_error:
            logger.warning(f"Erro ao verificar novas memórias: {str(verify_error)}")
            new_memories_added = True
        
        logger.info("Processamento de memórias concluído")
        
        # Adiciona confirmação explícita no console com detalhes
        timestamp = datetime.now().strftime("%H:%M:%S")
        user_message = message[:30] + "..." if len(message) > 30 else message
        
        if new_memories_added:
            print(f"\n💾 [{timestamp}] Nova memória adicionada ao Supabase:")
            print(f"   • Usuário: {user_id}")
            print(f"   • Conteúdo: \"{user_message}\"")
            print(f"   • Coleção: voxy_memories")
            print(f"   • Status: ✅ Sucesso")
        else:
            print(f"\n🔄 [{timestamp}] Memória existente utilizada (sem nova adição):")
            print(f"   • Usuário: {user_id}")
            print(f"   • Consulta: \"{user_message}\"")
            print(f"   • Memórias recuperadas: {len(relevant_memories['results'])}")
        
        return assistant_response
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        return f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"

def main():
    """Função principal para executar o assistente em modo CLI"""
    display_banner()
    
    try:
        # Verifica se o script de configuração já foi executado
        supabase_setup_path = os.path.join("utils", "setup_supabase.py")
        if os.path.exists(supabase_setup_path):
            print("🔧 Recomendação: Execute 'python utils/setup_supabase.py' antes de usar o agente")
            print("   Isso ajuda a verificar a conexão com o banco de dados.\n")
        
        # Inicializa os componentes
        openai_client, memory = setup_memory()
        
        user_id = input("👤 Digite seu ID de usuário (ou deixe em branco para 'default_user'): ").strip()
        if not user_id:
            user_id = "default_user"
        
        print(f"\n🚀 Conversa iniciada para o usuário: {user_id}")
        print("💡 Digite 'sair' para encerrar a conversa\n")
        
        while True:
            user_input = input("🧑 Você: ").strip()
            if not user_input:
                print("⚠️ Por favor, digite algo para conversar com o assistente.")
                continue
                
            if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                print("👋 Até logo!")
                break
            
            print("🤖 Assistente está pensando...", end="\r")
            response = chat_with_memories(
                message=user_input,
                user_id=user_id,
                openai_client=openai_client,
                memory=memory
            )
            
            print(" " * 40, end="\r")  # Limpa a linha do "pensando"
            print(f"🤖 Assistente: {response}\n")
    
    except ValueError as ve:
        print(f"❌ Erro de configuração: {str(ve)}")
        print("🔧 Por favor, configure as variáveis de ambiente conforme o .env.example")
    except KeyboardInterrupt:
        print("\n\n👋 Sessão encerrada pelo usuário.")
    except Exception as e:
        logger.error(f"Erro na execução principal: {str(e)}")
        print(f"❌ Ocorreu um erro crítico: {str(e)}")
        print("📋 Verifique os logs para mais detalhes.")
        print("\n🔧 Dica: Execute 'python utils/setup_supabase.py' para diagnosticar problemas de conexão.")

if __name__ == "__main__":
    main() 