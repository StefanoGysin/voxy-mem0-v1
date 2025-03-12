# Contribuindo com o Voxy-Mem0

Agradecemos seu interesse em contribuir com o Voxy-Mem0! Este documento fornece diretrizes para ajudá-lo a contribuir com o projeto.

## Código de Conduta

Ao participar deste projeto, você concorda em manter um ambiente respeitoso e construtivo para todos. Esperamos que todos os contribuidores sigam as boas práticas de desenvolvimento e comunicação.

## Como Contribuir

### Reportando Bugs

Se você encontrar um bug, por favor, crie uma issue no GitHub com as seguintes informações:

1. Título claro e descritivo
2. Passos detalhados para reproduzir o problema
3. Comportamento esperado vs. comportamento observado
4. Screenshots, se aplicável
5. Informações do seu ambiente (sistema operacional, versão do Python, etc.)

### Sugerindo Melhorias

Para sugerir melhorias, crie uma issue descrevendo:

1. Sua ideia de forma clara e concisa
2. Por que essa melhoria seria útil
3. Como você imagina que essa melhoria funcionaria

### Enviando Pull Requests

1. Faça um fork do repositório
2. Crie uma branch para sua contribuição (`git checkout -b feature/sua-feature`)
3. Implemente suas mudanças
4. Adicione ou atualize os testes conforme necessário
5. Atualize a documentação, se aplicável
6. Certifique-se de que os testes passam: `python -m unittest discover -s tests`
7. Faça commit das mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
8. Envie sua branch (`git push origin feature/sua-feature`)
9. Crie um Pull Request

## Padrões de Código

### Estilo de Código

Seguimos o [PEP 8](https://www.python.org/dev/peps/pep-0008/) para código Python.

- Use 4 espaços para indentação (não use tabs)
- Limite as linhas a 88 caracteres
- Use nomes descritivos para variáveis e funções
- Adicione docstrings para todas as funções, classes e módulos

### Testes

- Novas funcionalidades devem incluir testes
- Os testes existentes devem continuar passando
- Use unittest ou pytest para escrever testes

## Estrutura do Projeto

Antes de contribuir, familiarize-se com a estrutura do projeto:

```
voxy-mem0/
├── voxy_agent.py         # Código principal do assistente
├── examples/             # Exemplos de uso
├── logs/                 # Diretório para armazenamento de logs
├── tests/                # Testes automatizados
└── utils/                # Utilitários
```

## Processo de Desenvolvimento

1. Escolha uma issue para trabalhar ou crie uma nova
2. Discuta sua abordagem na issue antes de começar a implementação
3. Implemente sua solução em uma branch separada
4. Teste sua implementação localmente
5. Envie um Pull Request
6. Aguarde a revisão do código

## Dúvidas?

Se você tiver dúvidas sobre como contribuir, sinta-se à vontade para criar uma issue solicitando ajuda.

Agradecemos sua colaboração para tornar o Voxy-Mem0 melhor! 