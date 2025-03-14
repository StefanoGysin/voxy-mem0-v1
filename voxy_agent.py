from dotenv import load_dotenv
from openai import OpenAI
from mem0 import Memory
import os
import logging
import sys
from datetime import datetime
import colorama
from colorama import Fore, Style

# Informações da versão
__version__ = "1.0.0"
__author__ = "Voxy Team"

# Configuração de logging
log_path = os.path.join("logs", "voxy_agent.log")
os.makedirs(os.path.dirname(log_path), exist_ok=True)

# Classe personalizada para formatar logs com cores
class ColoredFormatter(logging.Formatter):
    """Formatador de logs com cores para melhor visualização"""

    COLORS = {
        'DEBUG': Fore.BLUE,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT
    }

    def __init__(self, fmt=None, datefmt=None, style='%', is_console=False):
        super().__init__(fmt, datefmt, style='%')
        self.is_console = is_console

    def format(self, record):
        # Formato padrão para arquivo de log (sem cores)
        log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        formatter = logging.Formatter(log_format)

        # Adiciona cores para saída no console
        if self.is_console:
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{Style.RESET_ALL}"
                record.msg = f"{self.COLORS[levelname]}{record.msg}{Style.RESET_ALL}"

        return formatter.format(record)

# Configura handlers com formatação personalizada
console_handler = logging.StreamHandler()
console_handler.setFormatter(ColoredFormatter(is_console=True))

file_handler = logging.FileHandler(log_path)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

# Configura o logger
logger = logging.getLogger("voxy-agent")
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)

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

    # Verifica se os objetos necessários foram fornecidos
    if openai_client is None:
        logger.error("Cliente OpenAI não fornecido")
        return "Erro: Cliente OpenAI não inicializado corretamente."

    if memory is None:
        logger.error("Memória não fornecida")
        return "Erro: Sistema de memória não inicializado corretamente."

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
            # Usa uma string não vazia para evitar erro na API de embeddings
            existing_memories_count = len(memory.search(query="consulta", user_id=user_id, limit=100)["results"])
            logger.info(f"Total existing memories: {existing_memories_count}")
        except Exception as search_error:
            logger.warning(f"Erro ao contar memórias existentes: {str(search_error)}")
            existing_memories_count = 0

        # Adiciona a nova memória
        try:
            add_result = memory.add(messages, user_id=user_id)
            logger.info(f"Memória adicionada com sucesso: {add_result}")
        except Exception as add_error:
            logger.error(f"Erro ao adicionar memória: {str(add_error)}")
            print(f"\n{Fore.RED}⚠️ AVISO: Falha ao salvar memória: {str(add_error)}{Style.RESET_ALL}")

        # Verifica se novas memórias foram adicionadas
        try:
            # Usa uma string não vazia para evitar erro na API de embeddings
            new_memories_count = len(memory.search(query="consulta", user_id=user_id, limit=100)["results"])
            new_memories_added = new_memories_count > existing_memories_count
        except Exception as verify_error:
            logger.warning(f"Erro ao verificar novas memórias: {str(verify_error)}")
            new_memories_added = True

        logger.info("Processamento de memórias concluído")

        # Inicializa o colorama para suporte a cores no terminal
        colorama.init()

        # Adiciona confirmação explícita no console com detalhes e cores
        timestamp = datetime.now().strftime("%H:%M:%S")
        user_message = message[:30] + "..." if len(message) > 30 else message

        # Barra separadora para melhor visualização
        separator = f"{Fore.CYAN}{'─' * 50}{Style.RESET_ALL}"

        if new_memories_added:
            print(separator)
            print(f"{Fore.GREEN}💾 [{timestamp}] Nova memória adicionada ao Supabase:{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   • Usuário:{Style.RESET_ALL} {user_id}")
            print(f"{Fore.YELLOW}   • Conteúdo:{Style.RESET_ALL} \"{user_message}\"")
            print(f"{Fore.YELLOW}   • Coleção:{Style.RESET_ALL} voxy_memories")
            print(f"{Fore.YELLOW}   • Status:{Style.RESET_ALL} {Fore.GREEN}✅ Sucesso{Style.RESET_ALL}")
            print(separator)
        else:
            print(separator)
            print(f"{Fore.BLUE}🔄 [{timestamp}] Memória existente utilizada (sem nova adição):{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}   • Usuário:{Style.RESET_ALL} {user_id}")
            print(f"{Fore.YELLOW}   • Consulta:{Style.RESET_ALL} \"{user_message}\"")
            print(f"{Fore.YELLOW}   • Memórias recuperadas:{Style.RESET_ALL} {len(relevant_memories['results'])}")
            print(separator)

        return assistant_response
    except Exception as e:
        logger.error(f"Erro ao processar mensagem: {str(e)}")
        return f"Desculpe, ocorreu um erro ao processar sua mensagem: {str(e)}"

def main():
    """Função principal para executar o assistente em modo CLI"""
    # Inicializa o colorama para suporte a cores no terminal
    colorama.init()

    display_banner()

    try:
        # Verifica se o script de configuração já foi executado
        supabase_setup_path = os.path.join("utils", "setup_supabase.py")
        if os.path.exists(supabase_setup_path):
            print(f"{Fore.CYAN}🔧 Recomendação:{Style.RESET_ALL} Execute 'python utils/setup_supabase.py' antes de usar o agente")
            print(f"   Isso ajuda a verificar a conexão com o banco de dados.\n")

        # Inicializa os componentes
        openai_client, memory = setup_memory()

        user_id = input(f"{Fore.CYAN}👤 Digite seu ID de usuário (ou deixe em branco para 'default_user'):{Style.RESET_ALL} ").strip()
        if not user_id:
            user_id = "default_user"

        print(f"\n{Fore.GREEN}🚀 Conversa iniciada para o usuário:{Style.RESET_ALL} {user_id}")
        print(f"{Fore.CYAN}💡 Digite 'sair' para encerrar a conversa{Style.RESET_ALL}\n")

        while True:
            user_input = input(f"{Fore.YELLOW}🧑 Você:{Style.RESET_ALL} ").strip()
            if not user_input:
                print(f"{Fore.RED}⚠️ Por favor, digite algo para conversar com o assistente.{Style.RESET_ALL}")
                continue

            if user_input.lower() in ['sair', 'exit', 'quit', 'q']:
                print(f"{Fore.CYAN}👋 Até logo!{Style.RESET_ALL}")
                break

            print(f"{Fore.BLUE}🤖 Assistente está pensando...{Style.RESET_ALL}", end="\r")
            response = chat_with_memories(
                message=user_input,
                user_id=user_id,
                openai_client=openai_client,
                memory=memory
            )

            print(" " * 40, end="\r")  # Limpa a linha do "pensando"
            print(f"{Fore.GREEN}🤖 Assistente:{Style.RESET_ALL} {response}\n")

    except ValueError as ve:
        error_box = f"{Fore.RED}{'═' * 60}\n❌ ERRO DE CONFIGURAÇÃO\n{'═' * 60}{Style.RESET_ALL}"
        print(f"\n{error_box}")
        print(f"{Fore.RED}Detalhes:{Style.RESET_ALL} {str(ve)}")
        print(f"{Fore.YELLOW}🔧 Por favor, configure as variáveis de ambiente conforme o .env.example{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═' * 60}{Style.RESET_ALL}")
    except KeyboardInterrupt:
        print(f"\n\n{Fore.CYAN}👋 Sessão encerrada pelo usuário.{Style.RESET_ALL}")
    except Exception as e:
        logger.error(f"Erro na execução principal: {str(e)}")
        error_box = f"{Fore.RED}{'═' * 60}\n❌ ERRO CRÍTICO\n{'═' * 60}{Style.RESET_ALL}"
        print(f"\n{error_box}")
        print(f"{Fore.RED}Detalhes:{Style.RESET_ALL} {str(e)}")
        print(f"{Fore.YELLOW}📋 Verifique os logs para mais detalhes.{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}🔧 Dica: Execute 'python utils/setup_supabase.py' para diagnosticar problemas de conexão.{Style.RESET_ALL}")
        print(f"{Fore.RED}{'═' * 60}{Style.RESET_ALL}")

if __name__ == "__main__":
    main()
