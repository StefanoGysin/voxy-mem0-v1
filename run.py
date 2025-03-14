#!/usr/bin/env python3
"""
Script unificado para executar o Voxy-Mem0.
Este script facilita as operações de configuração e execução do assistente Voxy-Mem0.

Comandos disponíveis:
    - test: Testa a conexão com o banco de dados
    - setup: Configura o banco de dados (cria extensões e estruturas necessárias)
    - run: Executa o assistente Voxy-Mem0 em modo CLI
    - web: Executa a interface web do Voxy-Mem0 com Streamlit
    - all: Executa setup e run em sequência
    - test-all: Executa os testes automatizados
    - system-info: Exibe informações do sistema
    - check-env: Verifica o ambiente de execução (dependências, variáveis, etc.)
"""

import os
import sys
import argparse
import importlib.util
import subprocess
from typing import List, Optional
import platform

# Informações da versão
__version__ = "1.0.0"

def display_banner():
    """Exibe o banner do utilitário"""
    banner = f"""
    ╔═══════════════════════════════════════════════╗
    ║                 VOXY-MEM0                     ║
    ║     Assistente com Memória Vetorial v{__version__}     ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)
    print("  🚀 Utilitário de linha de comando para o Voxy-Mem0")
    print("  🔧 Configuração, testes e execução simplificados")
    print("  📝 Documentação: https://github.com/StefanoGysin/voxy-mem0-v1\n")

def check_dependencies():
    """
    Verifica se todas as dependências necessárias estão instaladas.
    Se alguma dependência estiver faltando, pergunta ao usuário se deseja instalá-la.
    """
    print("📦 Verificando dependências do projeto...")

    # Mapeamento entre nomes de pacotes pip e nomes de módulos Python
    package_to_module = {
        'openai': 'openai',
        'python-dotenv': 'dotenv',
        'psycopg2-binary': 'psycopg2',
        'numpy': 'numpy',
        'mem0': 'mem0',
        'supabase': 'supabase',
        'vecs': 'vecs',
        'streamlit': 'streamlit',
        'streamlit-chat': 'streamlit_chat',
        'extra-streamlit-components': 'extra_streamlit_components'
    }

    required_packages = [
        'openai',
        'python-dotenv',
        'psycopg2-binary',
        'numpy',
        'mem0',
        'supabase',
        'vecs'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            # Tenta importar o pacote usando o nome correto do módulo
            module_name = package_to_module.get(package, package.replace('-', '_'))
            importlib.import_module(module_name)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"⚠️ Dependências em falta: {', '.join(missing_packages)}")

        response = input("Deseja instalar as dependências em falta? (s/n) ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            print("⏳ Instalando dependências...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
                print("✅ Dependências instaladas com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar dependências: {str(e)}")
                print(f"\n⚠️ Instale manualmente com: pip install {' '.join(missing_packages)}")
                return False
        else:
            print("\n⚠️ As dependências em falta são necessárias para executar o Voxy-Mem0.")
            print(f"⚠️ Instale manualmente com: pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ Todas as dependências estão instaladas!")

    return True

def check_env_file():
    """
    Verifica se o arquivo .env existe e contém as configurações necessárias.
    Se não existir, instrui o usuário a criá-lo.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    env_file = os.path.join(script_dir, '.env')

    if not os.path.exists(env_file):
        print("⚠️ Arquivo .env não encontrado!")
        print("Este arquivo é necessário para configurar as credenciais do Voxy-Mem0.")
        print("\nCrie um arquivo .env no diretório do projeto com o seguinte conteúdo:")
        print("""
# Configuração da OpenAI
# Obtenha sua chave de API em: https://platform.openai.com/account/api-keys
OPENAI_API_KEY=sua_chave_api_aqui

# Modelo da OpenAI a ser usado (padrão é gpt-4o-mini)
MODEL_CHOICE=gpt-4o-mini

# Configuração do Supabase para armazenamento vetorial
# Obtenha a URL de conexão do Database na seção Database do seu projeto Supabase
DATABASE_URL=postgres://postgres:SuaSenha@db.xxxxx.supabase.co:5432/postgres?sslmode=require

# Configuração do Supabase para autenticação (opcional - para versões futuras)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=sua_chave_anon_aqui

# Configurações adicionais
LOG_LEVEL=INFO
""")

        response = input("\nDeseja criar um arquivo .env básico agora? (s/n) ").strip().lower()
        if response in ['s', 'sim', 'y', 'yes']:
            try:
                with open(env_file, 'w') as f:
                    f.write("""# Configuração da OpenAI
# Obtenha sua chave de API em: https://platform.openai.com/account/api-keys
OPENAI_API_KEY=

# Modelo da OpenAI a ser usado (padrão é gpt-4o-mini)
MODEL_CHOICE=gpt-4o-mini

# Configuração do Supabase para armazenamento vetorial
# Obtenha a URL de conexão do Database na seção Database do seu projeto Supabase
DATABASE_URL=

# Configuração do Supabase para autenticação (opcional - para versões futuras)
SUPABASE_URL=
SUPABASE_KEY=

# Configurações adicionais
LOG_LEVEL=INFO
""")
                print(f"✅ Arquivo .env básico criado em: {env_file}")
                print("⚠️ Lembre-se de editar o arquivo para adicionar suas credenciais!")
            except Exception as e:
                print(f"❌ Erro ao criar arquivo .env: {str(e)}")
                return False
        else:
            print("⚠️ Um arquivo .env válido é necessário para continuar.")
            return False
    else:
        print("✅ Arquivo .env encontrado!")

    return True

def run_script(script_path, args=None):
    """
    Executa um script Python especificado com os argumentos fornecidos.

    Args:
        script_path: Caminho para o script Python a ser executado
        args: Lista de argumentos para passar ao script

    Returns:
        bool: True se o script foi executado com sucesso, False caso contrário
    """
    try:
        print(f"⏳ Executando: {os.path.basename(script_path)}...")

        cmd = [sys.executable, script_path]
        if args:
            cmd.extend(args)

        result = subprocess.run(cmd, check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o script {os.path.basename(script_path)}: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {str(e)}")
        return False

def run_tests():
    """
    Executa os testes automatizados do projeto.

    Returns:
        bool: True se os testes foram executados com sucesso, False caso contrário
    """
    print("\n🧪 Executando testes automatizados...")

    try:
        # Verifica se a pasta tests existe
        if not os.path.exists("tests"):
            print("❌ Diretório de testes não encontrado!")
            return False

        # Executa todos os testes no diretório tests
        result = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests"], check=False)

        if result.returncode == 0:
            print("✅ Todos os testes passaram com sucesso!")
            return True
        else:
            print("❌ Alguns testes falharam. Verifique os erros acima.")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar os testes: {str(e)}")
        return False

def show_system_info():
    """Exibe informações do sistema para diagnóstico"""
    print("\n🔍 Informações do Sistema:")
    print(f"  • Sistema Operacional: {platform.system()} {platform.release()}")
    print(f"  • Python: {platform.python_version()}")

    # Verifica as versões dos pacotes principais
    try:
        import openai
        print(f"  • OpenAI SDK: {openai.__version__}")
    except (ImportError, AttributeError):
        print("  • OpenAI SDK: Não instalado ou versão não disponível")

    try:
        import mem0
        print(f"  • Mem0: {mem0.__version__}")
    except (ImportError, AttributeError):
        print("  • Mem0: Não instalado ou versão não disponível")

    try:
        import psycopg2
        # O psycopg2 não expõe diretamente __version__, mas podemos usar a versão do módulo
        version = getattr(psycopg2, '__version__', 'Versão não disponível')
        print(f"  • Psycopg2: {version}")
    except ImportError:
        print("  • Psycopg2: Não instalado")

    print()

def main():
    """
    Função principal que processa os argumentos da linha de comando e executa
    as operações correspondentes.
    """
    parser = argparse.ArgumentParser(description='Script unificado para executar o Voxy-Mem0.')
    parser.add_argument('command', choices=['test', 'setup', 'run', 'web', 'all', 'test-all', 'system-info', 'check-env'],
                        help='Comando a ser executado: test, setup, run, web, all, test-all, system-info ou check-env')
    parser.add_argument('--interactive', '-i', action='store_true',
                        help='Executa em modo interativo (pergunta antes de cada passo)')

    # Verifica se há argumentos na linha de comando
    if len(sys.argv) == 1:
        display_banner()
        parser.print_help()
        return 0

    args = parser.parse_args()

    # Exibe o banner
    display_banner()

    # Processa o comando system-info separadamente pois não precisa das verificações iniciais
    if args.command == 'system-info':
        show_system_info()
        return 0

    # Processa o comando test-all separadamente pois não precisa das verificações iniciais
    if args.command == 'test-all':
        return 0 if run_tests() else 1

    # Processa o comando check-env separadamente pois usa seu próprio script
    if args.command == 'check-env':
        print("\n===== Verificando ambiente de execução =====")
        script_dir = os.path.dirname(os.path.abspath(__file__))
        check_env_script = os.path.join(script_dir, 'utils', 'check_environment.py')
        return 0 if run_script(check_env_script) else 1

    # Verifica as dependências e o arquivo .env antes de prosseguir
    if not check_dependencies():
        return 1

    if not check_env_file():
        return 1

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Executa o comando escolhido
    if args.command == 'test' or args.command == 'all':
        print("\n===== Testando conexão com o banco de dados =====")
        test_script = os.path.join(script_dir, 'utils', 'setup_supabase.py')
        if not run_script(test_script):
            if args.command == 'test':
                return 1
            elif args.interactive:
                response = input("\nO teste de conexão falhou. Deseja prosseguir com a configuração? (s/n) ").strip().lower()
                if response not in ['s', 'sim', 'y', 'yes']:
                    return 1

    if args.command == 'setup' or args.command == 'all':
        print("\n===== Configurando banco de dados =====")
        setup_script = os.path.join(script_dir, 'utils', 'setup_supabase.py')
        if not run_script(setup_script):
            if args.interactive:
                response = input("\nA configuração falhou. Deseja tentar executar o assistente mesmo assim? (s/n) ").strip().lower()
                if response not in ['s', 'sim', 'y', 'yes']:
                    return 1
            elif args.command == 'setup':
                return 1

    if args.command == 'run' or args.command == 'all':
        print("\n===== Executando o assistente Voxy-Mem0 (CLI) =====")
        voxy_script = os.path.join(script_dir, 'voxy_agent.py')
        return 0 if run_script(voxy_script) else 1

    if args.command == 'web':
        print("\n===== Executando a interface web do Voxy-Mem0 =====")
        web_script = os.path.join(script_dir, 'web', 'app.py')

        # Verifica se todas as dependências específicas da web estão instaladas
        web_dependencies = {
            'streamlit': 'streamlit>=1.32.0',
            'streamlit_chat': 'streamlit-chat>=0.1.1',
            'extra_streamlit_components': 'extra-streamlit-components>=0.1.60',
            'vecs': 'vecs>=0.2.6'
        }

        missing_web_deps = []
        for module, package in web_dependencies.items():
            try:
                importlib.import_module(module)
            except ImportError:
                missing_web_deps.append(package)

        # Instala dependências faltantes
        if missing_web_deps:
            print(f"⚠️ Dependências da interface web em falta: {', '.join(missing_web_deps)}")
            print("⏳ Instalando dependências da interface web...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_web_deps)
                print("✅ Dependências da interface web instaladas com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"❌ Erro ao instalar dependências da interface web: {str(e)}")
                print(f"⚠️ Instale manualmente com: pip install {' '.join(missing_web_deps)}")
                return 1

        try:
            # Executa o Streamlit com o script da aplicação web
            cmd = [sys.executable, "-m", "streamlit", "run", web_script, "--server.headless", "true"]
            print(f"Executando: {' '.join(cmd)}")
            return 0 if subprocess.run(cmd, check=True).returncode == 0 else 1
        except Exception as e:
            print(f"❌ Erro ao executar a interface web: {str(e)}")
            print(f"Detalhes do erro: {str(e)}")
            return 1

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Operação interrompida pelo usuário.")
        sys.exit(1)
