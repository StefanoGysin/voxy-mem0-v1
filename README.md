# Voxy-Mem0: Assistente com Memória Vetorial

![Versão](https://img.shields.io/badge/versão-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-green.svg)
![Licença](https://img.shields.io/badge/licença-MIT-yellow.svg)

## 📋 Visão Geral

Voxy-Mem0 é um assistente conversacional baseado em IA com memória vetorial de longo prazo. Desenvolvido com a biblioteca [Mem0](https://github.com/mem0ai/mem0) e integrado com a API da OpenAI e banco de dados Supabase, este assistente oferece uma experiência de conversação personalizada ao lembrar conversas anteriores, preferências e informações contextuais dos usuários.

<p align="center">
  <img src="https://github.com/mem0ai/mem0/raw/main/docs/public/logo.png" alt="Mem0 Logo" width="150"/>
</p>

## ✨ Funcionalidades

- **🧠 Memória Vetorial Persistente**: Armazena e recupera conversas anteriores usando embeddings
- **👤 Identificação de Usuários**: Permite múltiplos usuários com memórias individuais
- **🔒 Armazenamento Seguro**: Dados armazenados de forma segura no Supabase com pgvector
- **💬 Respostas Contextuais**: Gera respostas levando em consideração o histórico da conversa
- **📝 Logging Detalhado**: Sistema de registro para monitoramento e depuração
- **🚀 Fácil de Usar**: Interface de linha de comando simples e intuitiva

## 🛠️ Pré-requisitos

- Python 3.9+
- Conta na [OpenAI](https://platform.openai.com) com chave de API
- Projeto [Supabase](https://supabase.com) para armazenamento vetorial (plano gratuito é suficiente)

## 📦 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/StefanoGysin/voxy-mem0-v1.git
cd voxy-mem0-v1
```

### 2. Configure o Ambiente Virtual

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate

# Ativar ambiente virtual (macOS/Linux)
source .venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

1. Copie o arquivo `.env.example` para `.env`:

```bash
cp .env.example .env
```

2. Edite o arquivo `.env` com suas credenciais:
   - `OPENAI_API_KEY`: Sua chave de API da OpenAI
   - `DATABASE_URL`: URL de conexão do Supabase (veja instruções abaixo)
   - `MODEL_CHOICE`: Modelo da OpenAI (opcional, padrão é gpt-4o-mini)

### 5. Configure o Banco de Dados Supabase

1. Crie uma conta no [Supabase](https://supabase.com) caso ainda não tenha
2. Crie um novo projeto
3. Na interface do Supabase, vá até "Project Settings > Database"
4. Em "Connection string", selecione "URI" e copie a URL
5. Substitua `[YOUR-PASSWORD]` pela senha do seu banco de dados

**Importante para usuários Windows:** Adicione `?sslmode=require` ao final da URL.

## 🚀 Uso

### Modo Rápido com Script Unificado

O script unificado `run.py` oferece uma maneira fácil de executar o assistente:

```bash
# Teste a conexão com o banco de dados
python run.py test

# Configure o banco de dados (extensão pgvector)
python run.py setup

# Execute o assistente
python run.py run

# Ou execute todos os passos sequencialmente
python run.py all
```

### Modo Detalhado (Passo a Passo)

#### 1. Teste a Conexão com o Banco de Dados

```bash
python utils/test_connection.py
```

Este script irá testar diferentes métodos de conexão com o Supabase e recomendar o mais adequado para seu ambiente.

#### 2. Configure o Banco de Dados

```bash
python utils/setup_supabase.py
```

Este script verifica se a extensão pgvector está instalada e se a estrutura necessária está pronta.

#### 3. Execute o Assistente

```bash
python voxy_agent.py
```

Você será solicitado a fornecer um ID de usuário (ou usar o padrão "default_user"). Depois, você pode conversar com o assistente digitando mensagens.

## 💬 Exemplos de Interação

```
Você: Meu nome é João Silva
Assistente: Olá, João Silva! É um prazer conhecê-lo. Como posso ajudar você hoje?

Você: Eu moro em Lisboa
Assistente: Que legal, João! Lisboa é uma cidade maravilhosa com uma rica história e cultura. Há algo específico sobre Lisboa ou Portugal que você gostaria de conversar?

Você: Quem sou eu?
Assistente: Você é João Silva e você mora em Lisboa. Como posso ajudá-lo hoje?
```

## 🧪 Executando Testes

Para executar os testes automatizados:

```bash
python -m unittest test_agent.py
```

## 📁 Estrutura do Projeto

```
voxy-mem0-v1/
├── .env.example          # Modelo de variáveis de ambiente
├── .env                  # Variáveis de ambiente (local, não versionado)
├── .gitignore            # Arquivos ignorados no Git
├── LICENSE               # Licença do projeto
├── README.md             # Documentação do projeto
├── requirements.txt      # Dependências do projeto
├── run.py                # Script unificado de linha de comando
├── voxy_agent.py         # Código principal do assistente
├── examples/             # Exemplos de uso
│   ├── __init__.py       # Inicialização do módulo
│   └── api_example.py    # Exemplo de uso da API
├── logs/                 # Diretório para armazenamento de logs (não versionado)
│   └── __init__.py       # Mantém o diretório no repositório
├── tests/                # Testes automatizados
│   ├── __init__.py       # Inicialização do módulo
│   └── test_agent.py     # Testes do agente principal
└── utils/                # Utilitários
    └── setup_supabase.py # Script de configuração do banco de dados
```

## 🗺️ Desenvolvimento Futuro

- [ ] Interface web com Streamlit
- [ ] Sistema de autenticação de usuários
- [ ] Painel de administração para gerenciar memórias
- [ ] Suporte a entrada de imagens e áudio
- [ ] Integração com outras ferramentas e APIs
- [ ] Mais opções de armazenamento vetorial

## 🔍 Solução de Problemas

### Problemas de Conexão com o Banco de Dados

Se você tiver problemas ao conectar ao Supabase, tente os seguintes métodos de conexão:

#### Diferentes Formatos de URL

1. **Conexão Direta**
   ```
   postgres://postgres:[SENHA]@db.xxxxx.supabase.co:5432/postgres?sslmode=require
   ```

2. **Conexão via Session Pooler (Recomendada para Windows)**
   ```
   postgres://postgres.xxxxx:[SENHA]@aws-0-eu-central-2.pooler.supabase.co:5432/postgres?sslmode=require
   ```

3. **Conexão via Transaction Pooler**
   ```
   postgres://postgres.xxxxx:[SENHA]@aws-0-eu-central-2.pooler.supabase.com:6543/postgres?sslmode=require
   ```

#### Codificação de Caracteres Especiais

Se sua senha contém caracteres especiais, codifique-os corretamente:

| Caractere | Codificação |
|-----------|-------------|
| @ | %40 |
| ? | %3F |
| & | %26 |
| = | %3D |
| + | %2B |
| espaço | %20 |

### Erros com a API da OpenAI

Problemas comuns incluem:

1. Chave de API inválida ou expirada
2. Limite de requisições excedido
3. Créditos insuficientes na conta

## 📄 Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Mem0.ai](https://github.com/mem0ai/mem0) pela biblioteca de memória vetorial
- [OpenAI](https://openai.com) pelos modelos de linguagem
- [Supabase](https://supabase.com) pelo banco de dados com suporte vetorial 