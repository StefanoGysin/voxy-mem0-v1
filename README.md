# Voxy-Mem0: Assistente com Memória Vetorial

![Versão](https://img.shields.io/badge/versão-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/Python-3.12%2B-green.svg)
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
- **📝 Logging Colorido**: Sistema de registro avançado com formatação colorida para melhor visualização
- **🎨 Interface Amigável**: Interface de linha de comando com cores e formatação visual aprimorada
- **🚀 Fácil de Usar**: Experiência de usuário intuitiva com feedback visual claro

## 🛠️ Pré-requisitos

- Python 3.12+
- Conta na [OpenAI](https://platform.openai.com) com chave de API
- Projeto [Supabase](https://supabase.com) para armazenamento vetorial (plano gratuito é suficiente)

## 📦 Instalação

### 1. Clone o Repositório

```bash
git clone https://github.com/StefanoGysin/voxy-mem0-v1.git
cd voxy-mem0-v1
```

### 2. Configure o Ambiente Virtual

#### Windows
```powershell
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
.venv\Scripts\activate
```

#### macOS/Linux
```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual
source .venv/bin/activate
```

### 3. Instale as Dependências

```bash
# Atualizar pip para a versão mais recente
python -m pip install --upgrade pip

# Instalar todas as dependências
pip install -r requirements.txt
```

As principais dependências incluem:
- **mem0**: Biblioteca para gerenciamento de memória vetorial
- **openai**: Cliente oficial da API OpenAI
- **supabase**: Cliente Python para o Supabase
- **colorama**: Biblioteca para formatação colorida no terminal
- **python-dotenv**: Para carregamento de variáveis de ambiente

### 4. Configure as Variáveis de Ambiente

1. Copie o arquivo `.env.example` para `.env`:

```bash
# Windows
copy .env.example .env

# macOS/Linux
cp .env.example .env
```

2. Edite o arquivo `.env` com suas credenciais:
   - `OPENAI_API_KEY`: Sua chave de API da OpenAI
   - `DATABASE_URL`: URL de conexão do Supabase (veja instruções abaixo)
   - `MODEL_CHOICE`: Modelo da OpenAI (opcional, padrão é gpt-4o-mini)
   - `LOG_LEVEL`: Nível de logging (INFO, DEBUG, WARNING, ERROR)

### 5. Configure o Banco de Dados Supabase

1. Crie uma conta no [Supabase](https://supabase.com) caso ainda não tenha
2. Crie um novo projeto
3. Na interface do Supabase, vá até "Project Settings > Database"
4. Em "Connection string", selecione "URI" e copie a URL
5. Substitua `[YOUR-PASSWORD]` pela senha do seu banco de dados

#### Configuração por Sistema Operacional

**Windows:**
- Adicione `?sslmode=require` ao final da URL
- Exemplo: `postgres://postgres:MinhaSeNha123@db.xxxxx.supabase.co:5432/postgres?sslmode=require`
- Se encontrar erros de conexão, tente usar o Session Pooler: `postgres://postgres.xxxxx:[SENHA]@aws-0-eu-central-2.pooler.supabase.co:5432/postgres?sslmode=require`

**macOS/Linux:**
- A URL padrão geralmente funciona sem modificações
- Exemplo: `postgres://postgres:MinhaSeNha123@db.xxxxx.supabase.co:5432/postgres`
- Em caso de problemas, adicione `?sslmode=require` ao final da URL

## 🚀 Uso

### Modo Rápido com Script Unificado

O script unificado `run.py` oferece uma maneira fácil de executar o assistente:

```bash
# Teste a conexão com o banco de dados
python run.py test

# Configure o banco de dados (extensão pgvector)
python run.py setup

# Execute o assistente em modo CLI
python run.py run

# Execute a interface web com Streamlit
python run.py web

# Ou execute todos os passos sequencialmente
python run.py all

# Exibir informações do sistema
python run.py system-info
```

### Interface de Linha de Comando Aprimorada

A nova versão do Voxy-Mem0 inclui uma interface de linha de comando colorida e visualmente aprimorada:

#### Recursos Visuais
- **Formatação Colorida**: Textos, prompts e respostas com cores para melhor legibilidade
- **Separadores Visuais**: Delimitadores claros entre diferentes seções de saída
- **Indicadores de Status**: Ícones e cores para indicar sucesso, erro ou avisos
- **Logs Formatados**: Sistema de logging com cores diferentes para cada nível (INFO, WARNING, ERROR)

#### Exemplo de Saída
```
──────────────────────────────────────────────────────
💾 [00:51:00] Nova memória adicionada ao Supabase:
   • Usuário: web_user_24eca2a8
   • Conteúdo: "agora sabe quem eu sou?"
   • Coleção: voxy_memories
   • Status: ✅ Sucesso
──────────────────────────────────────────────────────
```

#### Tratamento de Erros Aprimorado
Em caso de erros, o sistema exibe mensagens de erro formatadas em caixas destacadas:

```
════════════════════════════════════════════════════════════
❌ ERRO DE CONFIGURAÇÃO
════════════════════════════════════════════════════════════
Detalhes: DATABASE_URL não configurado
🔧 Por favor, configure as variáveis de ambiente conforme o .env.example
════════════════════════════════════════════════════════════
```

### Interface Web com Streamlit

O Voxy-Mem0 agora inclui uma interface web moderna e intuitiva usando Streamlit:

```bash
# Execute a interface web
python run.py web
```

A interface web oferece:

- **🌐 Acesso via Navegador**: Acesse o assistente através de qualquer navegador
- **💬 Interface de Chat Amigável**: Interface de chat moderna e responsiva
- **👤 Gerenciamento de Usuários**: Troque facilmente entre diferentes IDs de usuário
- **⚙️ Configurações Personalizáveis**: Ajuste as configurações do assistente
- **📊 Visualização de Memórias**: Visualize as memórias armazenadas para seu usuário

Por padrão, a interface web estará disponível em `http://localhost:8501`

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
├── utils/                # Utilitários
│   └── setup_supabase.py # Script de configuração do banco de dados
└── web/                  # Interface web com Streamlit
    ├── __init__.py       # Inicialização do módulo
    ├── app.py            # Aplicação principal do Streamlit
    ├── components/       # Componentes reutilizáveis da UI
    │   ├── __init__.py
    │   └── sidebar.py    # Componente da barra lateral
    ├── pages/            # Páginas da aplicação
    │   ├── __init__.py
    │   ├── about.py      # Página sobre o projeto
    │   ├── chat.py       # Página de chat
    │   └── settings.py   # Página de configurações
    ├── static/           # Arquivos estáticos
    │   └── css/
    │       └── style.css # Estilos personalizados
    └── utils/            # Utilitários para a web
        ├── __init__.py
        ├── api.py        # Wrapper da API do Voxy-Mem0
        └── session.py    # Gerenciamento de sessão
```

## 🗺️ Desenvolvimento Futuro

- [x] Interface web com Streamlit
- [ ] Sistema de autenticação de usuários
- [ ] Painel de administração para gerenciar memórias
- [ ] Suporte a entrada de imagens e áudio
- [ ] Integração com outras ferramentas e APIs
- [ ] Mais opções de armazenamento vetorial

## 🎨 Melhorias Visuais e de Formatação

A versão mais recente do Voxy-Mem0 inclui diversas melhorias visuais e de formatação para tornar a experiência do usuário mais agradável e informativa:

### Sistema de Logging Colorido

O sistema de logging foi completamente reformulado para utilizar cores e formatação avançada:

- **Níveis de Log Coloridos**:
  - INFO: Verde 🟢
  - WARNING: Amarelo 🟡
  - ERROR: Vermelho 🔴
  - CRITICAL: Vermelho Brilhante 🔆

- **Formatação Estruturada**: Logs organizados com timestamps, categorias e mensagens claramente separados
- **Saída Dupla**: Logs são exibidos no console e também salvos em arquivo para referência futura

### Feedback Visual Aprimorado

- **Separadores Visuais**: Linhas horizontais coloridas para delimitar diferentes seções de saída
- **Caixas de Mensagem**: Mensagens importantes são exibidas em caixas destacadas
- **Ícones Informativos**: Uso de emojis e símbolos para indicar diferentes tipos de operações e status

### Tratamento de Erros Melhorado

- **Mensagens de Erro Detalhadas**: Erros são exibidos com informações detalhadas sobre a causa e possíveis soluções
- **Caixas de Erro Destacadas**: Erros críticos são exibidos em caixas vermelhas para chamar atenção
- **Sugestões de Solução**: Mensagens de erro incluem dicas sobre como resolver o problema

### Personalização

O sistema de cores pode ser personalizado editando as constantes `COLORS` na classe `ColoredFormatter` no arquivo `voxy_agent.py`:

```python
COLORS = {
    'DEBUG': Fore.BLUE,
    'INFO': Fore.GREEN,
    'WARNING': Fore.YELLOW,
    'ERROR': Fore.RED,
    'CRITICAL': Fore.RED + Style.BRIGHT
}
```

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

### Problemas com Formatação Colorida

Se você encontrar problemas com a formatação colorida no terminal:

1. **Cores não aparecem**: Alguns terminais não suportam cores ANSI. Tente usar um terminal diferente como Windows Terminal, PowerShell Core, ou terminais baseados em VT100.

2. **Caracteres estranhos**: Se você vir sequências de escape ANSI (como `\033[32m`) em vez de cores, seu terminal não está interpretando corretamente os códigos de cores.

3. **Solução para Windows**: No Windows, você pode precisar habilitar o suporte a ANSI:
   ```python
   # Isso é feito automaticamente pelo colorama.init()
   # Mas você pode forçar com:
   colorama.init(convert=True, strip=False, autoreset=False)
   ```

4. **Desabilitar cores**: Se preferir desabilitar as cores completamente, você pode editar o arquivo `voxy_agent.py` e remover ou comentar as linhas que inicializam o colorama.

### Erros com a API da OpenAI

Problemas comuns incluem:

1. Chave de API inválida ou expirada
2. Limite de requisições excedido
3. Créditos insuficientes na conta
4. Erro de formato na entrada para embeddings (corrigido na versão atual)

## 📄 Licença

Este projeto é licenciado sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 🙏 Agradecimentos

- [Mem0.ai](https://github.com/mem0ai/mem0) pela biblioteca de memória vetorial
- [OpenAI](https://openai.com) pelos modelos de linguagem
- [Supabase](https://supabase.com) pelo banco de dados com suporte vetorial
