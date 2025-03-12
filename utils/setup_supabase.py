"""
Utilitário para configurar o banco de dados Supabase para o Voxy-Mem0.
Este script verifica e cria a extensão pgvector necessária para o armazenamento vetorial.
"""

import os
import sys
import logging
from dotenv import load_dotenv
import psycopg2
from psycopg2 import sql
import time

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("setup-supabase")

# Versão do utilitário
__version__ = "1.0.0"

def check_connection(database_url, max_retries=3):
    """
    Verifica a conexão com o banco de dados com múltiplas tentativas
    
    Args:
        database_url: URL de conexão com o banco de dados
        max_retries: Número máximo de tentativas de conexão
        
    Returns:
        bool: True se a conexão for bem-sucedida, False caso contrário
    """
    logger.info("Verificando conexão com o banco de dados Supabase...")
    
    for attempt in range(1, max_retries + 1):
        try:
            conn = psycopg2.connect(database_url, connect_timeout=10)
            conn.close()
            logger.info("✅ Conexão estabelecida com sucesso!")
            return True
        except Exception as e:
            logger.warning(f"Tentativa {attempt}/{max_retries} falhou: {str(e)}")
            if attempt < max_retries:
                wait_time = 2 * attempt
                logger.info(f"Tentando novamente em {wait_time} segundos...")
                time.sleep(wait_time)
            else:
                logger.error("❌ Não foi possível conectar ao banco de dados após várias tentativas.")
                return False

def list_vector_collections(database_url):
    """
    Lista todas as coleções de vetores no banco de dados
    
    Args:
        database_url: URL de conexão com o banco de dados
        
    Returns:
        list: Lista de nomes das coleções encontradas
    """
    logger.info("Buscando coleções de vetores existentes...")
    collections = []
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Busca tabelas que começam com 'vecs_' (padrão do Supabase para coleções vetoriais)
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_name LIKE 'vecs_%'
            ORDER BY table_name;
        """)
        
        rows = cursor.fetchall()
        for row in rows:
            collection_name = row[0]
            # Remove o prefixo 'vecs_' para obter o nome real da coleção
            actual_name = collection_name[5:] if collection_name.startswith('vecs_') else collection_name
            collections.append({
                "table_name": collection_name,
                "collection_name": actual_name
            })
        
        if not collections:
            logger.info("Nenhuma coleção de vetores encontrada no banco de dados.")
        else:
            logger.info(f"Encontradas {len(collections)} coleções de vetores.")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        logger.error(f"Erro ao listar coleções: {str(e)}")
    
    return collections

def setup_database():
    """
    Configura o banco de dados Supabase para uso com o Voxy-Mem0.
    - Verifica a conexão
    - Cria a extensão pgvector se necessário
    - Lista coleções existentes
    
    Returns:
        bool: True se a configuração for bem-sucedida, False caso contrário
    """
    # Carrega variáveis de ambiente
    load_dotenv()
    
    # Verifica se a variável de ambiente DATABASE_URL está configurada
    database_url = os.environ.get('DATABASE_URL')
    if not database_url:
        logger.error("❌ Variável de ambiente DATABASE_URL não encontrada.")
        logger.error("Por favor, configure o arquivo .env com as informações corretas.")
        sys.exit(1)
    
    # Verifica conexão
    if not check_connection(database_url):
        return False
    
    try:
        # Conecta ao banco de dados
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        # Verifica se a extensão pgvector já está instalada
        cursor.execute("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector');")
        extension_exists = cursor.fetchone()[0]
        
        if extension_exists:
            logger.info("✅ Extensão pgvector já está instalada.")
        else:
            logger.info("⏳ Instalando extensão pgvector...")
            cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            logger.info("✅ Extensão pgvector instalada com sucesso!")
        
        # Verifica se a tabela de memórias existe
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_name = 'vecs_voxy_memories'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            logger.info("ℹ️ A tabela de memórias será criada automaticamente pelo mem0 na primeira execução.")
        else:
            logger.info("✅ Tabela de memórias (vecs_voxy_memories) já existe.")
        
        # Fecha a conexão
        cursor.close()
        conn.close()
        
        # Lista coleções existentes
        print("\nListando coleções de vetores...")
        collections = list_vector_collections(database_url)
        
        if collections:
            print("\n📊 Coleções de vetores encontradas:")
            print("-" * 50)
            print(f"{'Tabela':<30} {'Nome da Coleção':<20}")
            print("-" * 50)
            for coll in collections:
                print(f"{coll['table_name']:<30} {coll['collection_name']:<20}")
            print("-" * 50)
        else:
            print("\n⚠️ Nenhuma coleção de vetores encontrada.")
            print("   A coleção 'vecs_voxy_memories' será criada na primeira execução do agente.")
        
        logger.info("✅ Configuração do banco de dados concluída com sucesso!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Erro ao configurar o banco de dados: {str(e)}")
        logger.error("Verifique se a URL de conexão está correta e se o banco de dados está acessível.")
        
        # Dicas específicas para erros comuns
        error_str = str(e).lower()
        if "password authentication failed" in error_str:
            logger.error("📌 DICA: Verifique se a senha no DATABASE_URL está correta.")
        elif "could not connect to server" in error_str:
            logger.error("📌 DICA: Verifique se o servidor está online e acessível pela internet.")
        elif "connection refused" in error_str:
            logger.error("📌 DICA: Verifique se as regras de firewall permitem a conexão.")
        
        return False

def display_banner():
    """Exibe o banner do utilitário de configuração"""
    banner = f"""
    ╔═══════════════════════════════════════════════╗
    ║           CONFIGURAÇÃO SUPABASE               ║
    ║       Para Voxy-Mem0 - Memória Vetorial       ║
    ╚═══════════════════════════════════════════════╝
    """
    print(banner)
    print("  🔧 Utilitário de verificação e configuração da base de dados")
    print("  🔒 Configuração de extensões e tabelas necessárias")
    print("  📊 Diagnóstico de conexão e coleções vetoriais\n")

if __name__ == "__main__":
    display_banner()
    
    success = setup_database()
    
    if success:
        print("\n✅ Banco de dados configurado com sucesso!")
        print("   Todas as extensões necessárias estão instaladas.")
        print("   Você já pode executar o Voxy-Mem0 com 'python voxy_agent.py'")
    else:
        print("\n❌ Falha na configuração do banco de dados.")
        print("   Verifique os logs acima para detalhes do erro.")
        print("   Certifique-se de que:")
        print("   1. O arquivo .env está configurado corretamente")
        print("   2. A URL do banco de dados está correta")
        print("   3. O banco de dados está acessível pela internet")
        print("   4. As credenciais estão corretas") 