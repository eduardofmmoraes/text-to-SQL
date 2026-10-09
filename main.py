import psycopg2 as pg
import pandas as pd

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate

def execute_query(query: str) -> pd.DataFrame:
    with pg.connect(
        host="localhost",
        database="enterprise",
        user="admin",
        password="password",
        port=6543
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(query)
            data = cur.fetchall()
            columns = [c.name for c in cur.description]

    return pd.DataFrame(data, columns=columns)

def get_tables() -> list:
    tables = execute_query("""select concat(table_name,'(', string_agg(col, ', '), ')') from (select
        table_name, concat(column_name, ': ', data_type) as col
    from information_schema.columns
    where table_schema = 'public'
    order by table_name, ordinal_position
    )
    group by table_name""")
    
    return tables["concat"].tolist()

def get_initial_chat() -> list:
    chat = [
        ("system", "Você é um assistente de IA que traduz consultas em linguagem natural para consultas SQL, com o sgbd {sgbd}. "
                    "tabelas:\n{tabelas}. "
                    "Forneça apenas a consulta SQL sem explicações adicionais."
                    "Caso não seja especificado, arredonde números decimais para duas casas."
        ),
        ("human", "{query}")
    ]

    return chat

def main():
    load_dotenv()

    prompt = ChatPromptTemplate.from_messages(get_initial_chat())
    model = init_chat_model(model="google_genai:gemini-3.1-flash-lite")

    print("================================")
    user_request = input("O que você quer saber?\n")

    while user_request.lower() != "nada":
        chat_input = prompt.invoke({
            "sgbd": "PostgreSQL",
            "tabelas": get_tables(),
            "query": user_request
        }).to_messages()

        query = model.invoke(chat_input).text
        if query.lower().startswith("```sql"):
            query = query[6:-3].strip()

        print("QUERY:")
        print(query)
        print("RESULTADO:")
        print(execute_query(query))
        print("================================")
        user_request = input("O que você quer saber?\n")

if __name__ == "__main__":
    main()