from typing import List
from app.chains.ner_chain import ner_chain
from app.databases.neo4j_database.neo4j_database import get_tables_in_path
from app.openai.chat import chat_with_openai
from app.databases.postgres_database.database_connection import Table
from app.templates.sql_prompt import postgresql_template
from app.databases.qdrant_database.qdrant import search_embeddings


def create_sql_query(query: str):
    entities = ner_chain(query)
    tables, columns, values = [], [], []

    for elem in entities:
        tables.extend(search_embeddings(query=elem, search_type="table_name", score_threshold=0.6))
        columns.extend(search_embeddings(query=elem, search_type="column_name", score_threshold=0.8))
        values.extend(search_embeddings(query=elem, search_type="value", score_threshold=0.8))

    table_names: List[str] = [table["table_name"] for table in tables] + [col["table_name"] for col in columns]
    values: List[str] = [value["value"] for value in values]

    tables: List[Table] = []

    for table_from in table_names:
        for table_to in table_names:
            if table_from != table_to:
                tables.extend(get_tables_in_path(table_from, table_to))

    table_info = "\n".join([str(table) for table in tables])
    proper_nouns = ", ".join([f"{v['value']}" for v in values])

    sql_query = postgresql_template(table_info, proper_nouns, query)
    return chat_with_openai(sql_query)
