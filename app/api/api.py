from typing import List

from fastapi import FastAPI, HTTPException

from app.chains.ner_chain import ner_chain
from app.chains.sql_guardrail_chain import guardrail_chain
from app.neo4j_database.neo4j_database import get_neighbours, Node, get_tables_in_path
from app.openai.chat import chat_with_openai
from app.sql_database.database_connection import Table
from app.templates.sql_prompt import postgresql_template
from app.vectorstore.qdrant import search_embeddings

app = FastAPI()


@app.post("/getQuery/")
def get_sql_query(prompt: str):
    result = guardrail_chain(prompt)
    if result['verdict'] == "no":
        raise HTTPException(status_code=400, detail=result['reason'])
    response = create_query(prompt)

    return {"query": response}


def create_query(query: str):
    entities = ner_chain(query)
    tables, columns, values = [], [], []

    for elem in entities:
        tables.extend(search_embeddings(query=elem, search_type="table_name"))
        columns.extend(search_embeddings(query=elem, search_type="column_name"))
        values.extend(search_embeddings(query=elem, search_type="value"))

    table_names: List[str] = [table["table_name"] for table in tables] + [col["table_name"] for col in columns]
    values: List[str] = [value["value"] for value in values]

    tables: List[Table] = []

    for table_from in table_names:
        for table_to in table_names:
            if table_from != table_to:
                tables.extend(get_tables_in_path(table_from, table_to))

    table_info = "\n".join(tables)
    proper_nouns = ", ".join([f"{v['value']}" for v in values])

    sql_query = postgresql_template(table_info, proper_nouns, query)
    return chat_with_openai(sql_query)

# "How many users have purchased a bear bottle minimum 10 times?"
