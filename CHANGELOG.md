# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

## [1.0.0] - 2025-03-14

### Adicionado
- Interface de linha de comando com formatação colorida
- Sistema de logging avançado com cores para diferentes níveis de log
- Separadores visuais para melhor legibilidade no console
- Caixas de erro destacadas para mensagens de erro
- Verificações de objetos nulos para evitar erros de referência
- Testes para as novas funcionalidades de formatação colorida
- Documentação detalhada no README.md
- Arquivo CHANGELOG.md para documentar mudanças

### Corrigido
- Erro na API de embeddings ao usar strings vazias como consulta
- Tratamento de erros aprimorado com mensagens mais descritivas
- Verificações de segurança para evitar vazamento de credenciais

### Alterado
- Atualização da documentação para refletir as novas funcionalidades
- Melhoria na estrutura de arquivos para facilitar a manutenção
- Otimização do código para melhor desempenho
- Atualização dos testes para cobrir as novas funcionalidades

### Segurança
- Garantia de que credenciais sensíveis não sejam incluídas no repositório
- Configuração adequada do .gitignore para excluir arquivos sensíveis
- Uso de variáveis de ambiente para armazenar credenciais
