#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Utilitário para verificar o ambiente de execução do Voxy-Mem0.
Este script verifica se todas as dependências estão instaladas corretamente
e se o ambiente está configurado adequadamente.
"""

import os
import sys
import platform
import logging
import importlib.util
from dotenv import load_dotenv
import subprocess
import pkg_resources

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("check-environment")

# Versão do utilitário
__version__ = "1.0.0"

# Lista de dependências essenciais
ESSENTIAL_PACKAGES = [
    "openai",
    "mem0",
    "python-dotenv",
    "colorama",
    "supabase",
    "pgvector",
    "sqlalchemy",
    "pydantic",
    "requests",
    "tqdm",
    "numpy",
    "streamlit"
]

def check_python_version():
    """
    Verifica se a versão do Python é compatível.

    Returns:
        bool: True se a versão for compatível, False caso contrário
    """
    logger.info("Verificando versão do Python...")

    python_version = platform.python_version()
    major, minor, _ = map(int, python_version.split('.'))

    if major >= 3 and minor >= 12:
        logger.info(f"✅ Versão do Python: {python_version} (compatível)")
        return True
    else:
        logger.error(f"❌ Versão do Python: {python_version}")
        logger.error("O Voxy-Mem0 requer Python 3.12 ou superior.")
        return False

def check_dependencies():
    """
    Verifica se todas as dependências estão instaladas.

    Returns:
        bool: True se todas as dependências estiverem instaladas, False caso contrário
    """
    logger.info("Verificando dependências...")

    missing_packages = []
    installed_packages = {}

    # Obtém a lista de pacotes instalados
    try:
        installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    except Exception as e:
        logger.error(f"Erro ao obter pacotes instalados: {str(e)}")
        return False

    # Verifica cada pacote essencial
    for package in ESSENTIAL_PACKAGES:
        package_lower = package.lower()
        if package_lower in installed:
            installed_packages[package] = installed[package_lower]
        else:
            missing_packages.append(package)

    # Exibe os pacotes instalados
    if installed_packages:
        logger.info("Pacotes instalados:")
        for package, version in installed_packages.items():
            logger.info(f"  ✅ {package}: {version}")

    # Exibe os pacotes ausentes
    if missing_packages:
        logger.error("Pacotes ausentes:")
        for package in missing_packages:
            logger.error(f"  ❌ {package}")

        logger.error("\nInstale os pacotes ausentes com:")
        logger.error(f"pip install {' '.join(missing_packages)}")
        return False

    logger.info("✅ Todas as dependências estão instaladas.")
    return True

def check_environment_variables():
    """
    Verifica se as variáveis de ambiente necessárias estão configuradas.

    Returns:
        bool: True se todas as variáveis estiverem configuradas, False caso contrário
    """
    logger.info("Verificando variáveis de ambiente...")

    # Carrega variáveis de ambiente do arquivo .env
    load_dotenv()

    # Lista de variáveis essenciais
    essential_vars = [
        "OPENAI_API_KEY",
        "DATABASE_URL"
    ]

    # Lista de variáveis opcionais
    optional_vars = [
        "MODEL_CHOICE",
        "SUPABASE_URL",
        "SUPABASE_KEY",
        "LOG_LEVEL",
        "DISABLE_COLORS"
    ]

    # Verifica variáveis essenciais
    missing_vars = []
    for var in essential_vars:
        if not os.environ.get(var):
            missing_vars.append(var)

    # Exibe status das variáveis essenciais
    if not missing_vars:
        logger.info("✅ Todas as variáveis de ambiente essenciais estão configuradas.")
    else:
        logger.error("❌ Variáveis de ambiente essenciais ausentes:")
        for var in missing_vars:
            logger.error(f"  - {var}")
        logger.error("\nConfigure as variáveis ausentes no arquivo .env")
        return False

    # Exibe status das variáveis opcionais
    configured_optional_vars = []
    for var in optional_vars:
        if os.environ.get(var):
            configured_optional_vars.append(var)

    if configured_optional_vars:
        logger.info("Variáveis de ambiente opcionais configuradas:")
        for var in configured_optional_vars:
            logger.info(f"  - {var}")

    return True

def check_system_info():
    """
    Exibe informações sobre o sistema.
    """
    logger.info("Coletando informações do sistema...")

    # Sistema operacional
    os_name = platform.system()
    os_version = platform.version()
    logger.info(f"Sistema Operacional: {os_name} {os_version}")

    # Arquitetura
    architecture = platform.architecture()[0]
    logger.info(f"Arquitetura: {architecture}")

    # Processador
    processor = platform.processor()
    if processor:
        logger.info(f"Processador: {processor}")

    # Python
    python_version = platform.python_version()
    python_implementation = platform.python_implementation()
    logger.info(f"Python: {python_implementation} {python_version}")

    # Ambiente virtual
    venv = os.environ.get('VIRTUAL_ENV')
    if venv:
        logger.info(f"Ambiente Virtual: {os.path.basename(venv)}")
    else:
        logger.warning("Ambiente Virtual: Não detectado")

    # Diretório de trabalho
    cwd = os.getcwd()
    logger.info(f"Diretório de Trabalho: {cwd}")

def display_banner():
    """Exibe o banner do utilitário de verificação de ambiente"""
    banner = f"""
    ╔═══════════════════════════════════════════════╗
    ║           VERIFICAÇÃO DE AMBIENTE             ║
    ║       Para Voxy-Mem0 - Memória Vetorial       ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)
    print("  🔍 Utilitário de verificação do ambiente de execução")
    print("  🔧 Verificação de dependências e configurações")
    print("  📊 Diagnóstico de compatibilidade\n")

def main():
    """
    Função principal que executa todas as verificações.

    Returns:
        int: 0 se todas as verificações passarem, 1 caso contrário
    """
    display_banner()

    # Lista de verificações
    checks = [
        ("Versão do Python", check_python_version),
        ("Dependências", check_dependencies),
        ("Variáveis de Ambiente", check_environment_variables)
    ]

    # Executa as verificações
    all_passed = True
    for name, check_func in checks:
        print(f"\n{'=' * 50}")
        print(f"Verificando: {name}")
        print(f"{'-' * 50}")

        try:
            result = check_func()
            if not result:
                all_passed = False
        except Exception as e:
            logger.error(f"Erro durante a verificação de {name}: {str(e)}")
            all_passed = False

    # Exibe informações do sistema
    print(f"\n{'=' * 50}")
    print("Informações do Sistema")
    print(f"{'-' * 50}")
    check_system_info()

    # Exibe resultado final
    print(f"\n{'=' * 50}")
    if all_passed:
        print("✅ Todas as verificações passaram!")
        print("O ambiente está configurado corretamente para executar o Voxy-Mem0.")
        return 0
    else:
        print("❌ Algumas verificações falharam.")
        print("Corrija os problemas acima antes de executar o Voxy-Mem0.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
