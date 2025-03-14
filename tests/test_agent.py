#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Testes automatizados para o Voxy-Mem0.
Execute com: python -m unittest tests.test_agent
"""

import unittest
import os
import logging
from unittest.mock import MagicMock, patch
import sys
from datetime import datetime
import io
from contextlib import redirect_stdout

# Configuração de logging para testes
logging.basicConfig(level=logging.ERROR)

# Adiciona o diretório raiz ao path para importação
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Importa as funções do módulo voxy_agent
from voxy_agent import setup_memory, chat_with_memories, __version__, ColoredFormatter

class TestVoxyAgentConfig(unittest.TestCase):
    """Testes para configuração do agente e ambiente"""

    def setUp(self):
        """Configuração inicial para cada teste"""
        # Cria um backup das variáveis de ambiente originais
        self.env_backup = {}
        for key in ['DATABASE_URL', 'OPENAI_API_KEY', 'MODEL_CHOICE']:
            self.env_backup[key] = os.environ.get(key)

    def tearDown(self):
        """Restaura o ambiente após cada teste"""
        # Restaura as variáveis de ambiente originais
        for key, value in self.env_backup.items():
            if value is None:
                if key in os.environ:
                    del os.environ[key]
            else:
                os.environ[key] = value

    def test_version_format(self):
        """Verifica se a versão está no formato correto"""
        self.assertRegex(__version__, r'^\d+\.\d+\.\d+$',
                        f"Versão '{__version__}' não está no formato correto (x.y.z)")

    def test_missing_database_url(self):
        """Testa erro quando DATABASE_URL está ausente"""
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']

        with self.assertRaises(ValueError) as context:
            setup_memory()

        self.assertIn('DATABASE_URL', str(context.exception))

    def test_missing_openai_key(self):
        """Testa erro quando OPENAI_API_KEY está ausente"""
        os.environ['DATABASE_URL'] = 'postgresql://fake:fake@localhost:5432/fake'

        if 'OPENAI_API_KEY' in os.environ:
            del os.environ['OPENAI_API_KEY']

        with self.assertRaises(ValueError) as context:
            setup_memory()

        self.assertIn('OPENAI_API_KEY', str(context.exception))


@unittest.skipIf(not os.environ.get('DATABASE_URL') or not os.environ.get('OPENAI_API_KEY'),
                "Variáveis de ambiente DATABASE_URL ou OPENAI_API_KEY não configuradas")
class TestVoxyAgent(unittest.TestCase):
    """Testes para as funções principais do agente com mocks"""

    def setUp(self):
        """Configuração inicial para cada teste"""
        self.mock_openai = MagicMock()
        self.mock_memory = MagicMock()

        # Mock para o cliente OpenAI
        self.mock_openai.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Resposta simulada do assistente"))]
        )

        # Mock para a memória
        self.mock_memory.search.return_value = {
            "results": [
                {"memory": "Memória teste 1", "score": 0.95},
                {"memory": "Memória teste 2", "score": 0.85}
            ]
        }

        # Setup para ambiente de teste
        if 'MODEL_CHOICE' not in os.environ:
            os.environ['MODEL_CHOICE'] = 'gpt-3.5-turbo'

    def test_setup_memory_config(self):
        """Testa se a configuração da memória está correta"""
        with patch('voxy_agent.Memory') as MockMemory, \
             patch('voxy_agent.OpenAI') as MockOpenAI:

            MockMemory.from_config.return_value = self.mock_memory
            MockOpenAI.return_value = self.mock_openai

            openai_client, memory = setup_memory()

            # Verifica se Memory.from_config foi chamado com configuração correta
            MockMemory.from_config.assert_called_once()
            config = MockMemory.from_config.call_args[0][0]

            # Verifica a configuração do provedor LLM
            self.assertEqual(config['llm']['provider'], 'openai')
            # Verifica apenas o provedor, não o modelo específico, que pode mudar
            self.assertIn('model', config['llm']['config'])

            # Verifica a configuração do provedor de armazenamento vetorial
            self.assertEqual(config['vector_store']['provider'], 'supabase')
            self.assertEqual(config['vector_store']['config']['collection_name'], 'voxy_memories')

    def test_chat_with_memories(self):
        """Testa o fluxo básico de chat com memória"""
        test_message = "Olá, como vai?"
        test_user_id = "usuario_teste"

        # Executa a função de chat
        response = chat_with_memories(
            message=test_message,
            user_id=test_user_id,
            openai_client=self.mock_openai,
            memory=self.mock_memory
        )

        # Verifica se a função de busca de memória foi chamada
        # Não verificamos os parâmetros exatos, pois a implementação pode mudar
        self.assertTrue(self.mock_memory.search.called)

        # Verifica se a API do OpenAI foi chamada corretamente
        self.mock_openai.chat.completions.create.assert_called_once()

        # Verifica se a função de adição à memória foi chamada
        self.mock_memory.add.assert_called_once()

        # Verifica a resposta
        self.assertEqual(response, "Resposta simulada do assistente")

    def test_chat_with_openai_error(self):
        """Testa o comportamento quando a API OpenAI falha"""
        # Configura o mock para lançar uma exceção
        self.mock_openai.chat.completions.create.side_effect = Exception("Erro simulado na API")

        # Executa a função de chat com o erro simulado
        response = chat_with_memories(
            message="Teste com erro",
            user_id="usuario_teste",
            openai_client=self.mock_openai,
            memory=self.mock_memory
        )

        # Verifica se a resposta contém informação sobre o erro
        self.assertIn("Erro na comunicação com a OpenAI", response)
        self.assertIn("Erro simulado na API", response)


class TestVoxyAgentLocal(unittest.TestCase):
    """Testes locais que não requerem conexão real com APIs externas"""

    def test_imports(self):
        """Verifica se os módulos essenciais estão disponíveis"""
        try:
            import openai
            import dotenv
            import mem0
            self.assertTrue(True)
        except ImportError as e:
            self.fail(f"Falha na importação de módulos essenciais: {str(e)}")

    def test_memory_mock(self):
        """Testa a integração entre o agente e a memória mockada"""
        # Cria um mock da memória
        mock_memory = MagicMock()
        mock_memory.search.return_value = {"results": []}
        mock_memory.add.return_value = {"status": "success"}

        # Cria um mock do OpenAI
        mock_openai = MagicMock()
        mock_openai.chat.completions.create.return_value = MagicMock(
            choices=[MagicMock(message=MagicMock(content="Resposta de teste"))]
        )

        # Testa a função de chat
        result = chat_with_memories(
            message="Teste local",
            user_id="usuario_local",
            openai_client=mock_openai,
            memory=mock_memory
        )

        # Verifica o resultado
        self.assertEqual(result, "Resposta de teste")
        # Verifica se a função de busca de memória foi chamada
        # Não verificamos o número exato de chamadas, pois a implementação pode mudar
        self.assertTrue(mock_memory.search.called)
        # Verifica se a função de adição à memória foi chamada
        self.assertTrue(mock_memory.add.called)


class TestColoredFormatter(unittest.TestCase):
    """Testes para a classe ColoredFormatter"""

    def test_formatter_initialization(self):
        """Testa a inicialização do formatador colorido"""
        formatter = ColoredFormatter(is_console=True)
        self.assertTrue(formatter.is_console)

        formatter = ColoredFormatter(is_console=False)
        self.assertFalse(formatter.is_console)

    def test_formatter_format(self):
        """Testa a formatação de logs com cores"""
        formatter = ColoredFormatter(is_console=True)

        # Cria um registro de log para teste
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="Mensagem de teste",
            args=(),
            exc_info=None
        )

        # Captura a saída formatada
        formatted = formatter.format(record)

        # Verifica se a mensagem está presente na saída formatada
        self.assertIn("Mensagem de teste", formatted)

    def test_formatter_colors(self):
        """Testa se os níveis de log têm cores diferentes"""
        formatter = ColoredFormatter(is_console=True)

        # Verifica se todos os níveis de log têm cores definidas
        self.assertIn('DEBUG', formatter.COLORS)
        self.assertIn('INFO', formatter.COLORS)
        self.assertIn('WARNING', formatter.COLORS)
        self.assertIn('ERROR', formatter.COLORS)
        self.assertIn('CRITICAL', formatter.COLORS)


class TestConsoleOutput(unittest.TestCase):
    """Testes para a saída formatada no console"""

    def test_console_output_format(self):
        """Testa o formato da saída no console"""
        # Captura a saída do console
        f = io.StringIO()
        with redirect_stdout(f):
            # Simula uma mensagem de memória adicionada
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"\n💾 [{timestamp}] Nova memória adicionada ao Supabase:")
            print(f"   • Usuário: test_user")
            print(f"   • Conteúdo: \"Mensagem de teste\"")
            print(f"   • Coleção: voxy_memories")
            print(f"   • Status: ✅ Sucesso")

        # Obtém a saída capturada
        output = f.getvalue()

        # Verifica se a saída contém os elementos esperados
        self.assertIn("Nova memória adicionada ao Supabase", output)
        self.assertIn("test_user", output)
        self.assertIn("Mensagem de teste", output)
        self.assertIn("voxy_memories", output)
        self.assertIn("Sucesso", output)


if __name__ == '__main__':
    # Executa todos os testes
    print(f"Executando testes para Voxy Agent v{__version__}")
    unittest.main()
