# Text-to-SQL

Assistente de linha de comando que traduz perguntas em linguagem natural para consultas SQL (PostgreSQL), executa a consulta e exibe o resultado. Usa LangChain com um modelo local servido pelo [LM Studio](https://lmstudio.ai/) (`qwen/qwen3.6-35b-a3b`), que pode rodar na própria máquina ou em outra máquina via [LM Link](https://lmstudio.ai/link).

## Como funciona

1. Lê o esquema do banco (`information_schema`) e o envia ao modelo junto com a pergunta.
2. O modelo devolve apenas a consulta SQL, que é salva em [query.sql](query.sql).
3. A consulta é executada e o resultado é exibido como DataFrame do pandas.
4. O histórico da conversa é mantido, então dá para fazer perguntas de acompanhamento.

## Banco de dados

Um PostgreSQL 18 via Docker, populado por [init.sql](init.sql) com dados fictícios de uma empresa: `setores`, `cargos`, `funcionarios`, `projetos`, `alocacoes` e `pagamentos`. A aplicação conecta com o usuário `gemini`, que só tem permissão de `SELECT`.

## Modelo (LM Studio + LM Link)

O modelo é acessado pela API compatível com OpenAI do servidor local do LM Studio, em `http://localhost:1235/v1`.

Com o **LM Link**, o modelo pode ficar carregado em outra máquina (por exemplo, um PC com GPU) e aparecer no LM Studio local como se fosse local. O próprio LM Studio cuida da conexão entre as máquinas, que é criptografada e não expõe portas na internet. Não é preciso configurar VPN nem redirecionamento de portas. Assim o código não muda: ele sempre fala com `localhost`, e o LM Studio encaminha as requisições para a máquina remota.

Para configurar:

1. Instale o LM Studio nas duas máquinas e entre com a mesma conta. O LM Link ainda está em *preview* e o acesso precisa ser solicitado em [lmstudio.ai/link](https://lmstudio.ai/link).
2. Ative o LM Link nas duas máquinas, pelo app ou com `lms link`. A máquina remota pode rodar sem interface, usando o daemon `llmster`.
3. Na máquina local, carregue o modelo `qwen/qwen3.6-35b-a3b` (ele aparece no seletor de modelos marcado como remoto).
4. Inicie o servidor local na porta `1235`, que é a porta usada em [main.py](main.py). O padrão do LM Studio é `1234`; para usá-lo, altere o `base_url` em `main.py`.

Para usar outro modelo, troque o `model` em `main.py` pelo identificador que o LM Studio exibe, mantendo o prefixo `openai:`.

## Requisitos

- Python 3.12+ e [uv](https://docs.astral.sh/uv/)
- Docker com Docker Compose
- LM Studio (e, opcionalmente, uma segunda máquina conectada via LM Link)

## Uso

```bash
# 1. Subir o banco (porta 6543)
docker compose up -d

# 2. Garantir que o servidor do LM Studio está rodando em localhost:1235 com o modelo carregado

# 3. Rodar
uv run main.py
```

Digite sua pergunta (ex.: *"Qual o salário médio por setor?"*) e digite `nada` para sair.

> ⚠️ As consultas geradas são executadas diretamente no banco, sem validação. O usuário `gemini` só tem permissão de leitura, mas use apenas em ambiente de testes.
