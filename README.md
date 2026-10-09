# Text-to-SQL

Assistente de linha de comando que traduz perguntas em linguagem natural para consultas SQL (PostgreSQL), executa a consulta e exibe o resultado. Usa LangChain com o modelo Gemini (`gemini-3.1-flash-lite`).

## Como funciona

1. Lê o esquema do banco (`information_schema`) e o envia ao modelo junto com a pergunta.
2. O modelo devolve apenas a consulta SQL.
3. A consulta é executada e o resultado é exibido como DataFrame do pandas.

## Banco de dados

Um PostgreSQL 18 via Docker, populado por [init.sql](init.sql) com dados fictícios de uma empresa: `setores`, `cargos`, `funcionarios`, `projetos`, `alocacoes` e `pagamentos`.

## Requisitos

- Python 3.12+ e [uv](https://docs.astral.sh/uv/)
- Docker com Docker Compose
- Chave da API do Google Gemini

## Uso

```bash
# 1. Subir o banco (porta 6543)
docker compose up -d

# 2. Configurar a chave da API
echo "GOOGLE_API_KEY=sua-chave" > .env

# 3. Rodar
uv run main.py
```

Digite sua pergunta (ex.: *"Qual o salário médio por setor?"*) e digite `nada` para sair.

> ⚠️ As consultas geradas são executadas diretamente no banco, sem validação. Use apenas em ambiente de testes.
