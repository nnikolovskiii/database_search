from fastapi import FastAPI, HTTPException

from app.chains.ner_chain import ner_chain
from app.chains.sql_guardrail_chain import guardrail_chain
from app.neo4j_database.neo4j_database import get_neighbours, Node
from app.openai.chat import chat_with_openai
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
    extracted_info = ner_chain(query)
    tables, columns, values = [], [], []

    for elem in extracted_info:
        table_results = search_embeddings(query=elem, search_type="table_name")
        column_results = search_embeddings(query=elem, search_type="column_name")
        value_results = search_embeddings(query=elem, search_type="value")

        for result in table_results:
            tables.extend(get_neighbours(Node(type="Table", properties=result)))
        for result in column_results:
            columns.extend(get_neighbours(Node(type="Column", properties=result)))
        for result in value_results:
            values.extend(get_neighbours(Node(type="Value", properties=result)))

    table_info = "\n".join([f"Table: {t['table_name']}, Columns: {t['columns']}" for t in tables])
    proper_nouns = "\n".join([f"{v['value']}" for v in values])

    sql_query = postgresql_template(table_info, proper_nouns, query)
    return chat_with_openai(sql_query)


# Query = "How many users have pruchased a bear bottle minimum 10 times?"
# main(Query)
