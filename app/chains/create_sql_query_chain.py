import json
from typing import List, Set
from app.chains.ner_chain import ner_chain
from app.chains.validate_info_chain import validate_info_chain
from app.databases.neo4j_database.neo4j_database import get_tables_in_path
from app.models.outputs import SqlGenerationOutput, ValidationOutput
from app.openai.chat import chat_with_openai
from app.databases.postgres_database.database_connection import Table, run_query
from app.templates.create_sql_prompt import postgresql_template
from app.databases.qdrant_database.qdrant import search_embeddings, SearchOutput
from app.utils.json_extraction import trim_and_load_json


def create_sql_query(collection_name: str, query: str) -> str:
    try:
        entities = ner_chain(query)
        tables_objs, columns_objs, values_objs = extract_search_objects(entities, collection_name)

        tables = gather_tables_from_paths(tables_objs, columns_objs, collection_name)
        table_info = format_table_info(tables)

        validation_output = validate_info_chain(table_info=table_info, question=query)
        if validation_output.verdict == "no":
            tables.update(find_missing_tables(validation_output, collection_name))

        table_info = format_table_info(tables)
        proper_nouns = format_proper_nouns(values_objs)
        sql_query = generate_sql_query(table_info, proper_nouns, query)

        return execute_and_return_query_results(collection_name, sql_query)

    except Exception as e:
        return json.dumps({"error": str(e)})


def extract_search_objects(entities: List[str], collection_name: str):
    tables_objs, columns_objs, values_objs = [], [], []

    for entity in entities:
        tables_objs.extend(search_embeddings(query=entity, search_type="table_name", score_threshold=0.2, top_k=3,
                                             collection_name=collection_name))
        columns_objs.extend(search_embeddings(query=entity, search_type="column_name", score_threshold=0.2, top_k=3,
                                              collection_name=collection_name))
        values_objs.extend(search_embeddings(query=entity, search_type="value", score_threshold=0.8, top_k=3,
                                             collection_name=collection_name))

    return tables_objs, columns_objs, values_objs


def gather_tables_from_paths(tables_objs: List[SearchOutput], columns_objs: List[SearchOutput], collection_name: str) -> \
        Set[Table]:
    table_names = {table.table_name for table in tables_objs} | {col.table_name for col in columns_objs}
    return _get_tables_in_paths(table_names, collection_name)


def format_table_info(tables: Set[Table]) -> str:
    return "\n".join([str(table) for table in tables])


def format_proper_nouns(values_objs: List[SearchOutput]) -> str:
    return ", ".join([value.value for value in values_objs])


def generate_sql_query(table_info: str, proper_nouns: str, query: str) -> SqlGenerationOutput:
    sql_prompt = postgresql_template(table_info, proper_nouns, query)
    chat_output = chat_with_openai(sql_prompt)
    json_data = trim_and_load_json(input_string=chat_output)
    sql_output = SqlGenerationOutput(**json_data)
    return sql_output


def execute_and_return_query_results(collection_name: str, sql_output: SqlGenerationOutput) -> str:
    results = run_query(collection_name, sql_output)
    if isinstance(results, str):
        return json.dumps({"message": results})

    return json.dumps({"query": sql_output.query, "output": results})


def find_missing_tables(validation_output: ValidationOutput, collection_name: str) -> Set[Table]:
    missing_tables_objs = set()

    for table in validation_output.missing_tables:
        missing_tables_objs.update(search_embeddings(query=table, search_type="table_name", score_threshold=0.2,
                                                     collection_name=collection_name))

    return _get_tables_in_paths({table.table_name for table in missing_tables_objs}, collection_name)


def _get_tables_in_paths(table_names: Set[str], collection_name: str) -> Set[Table]:
    tables = set()

    for table_from in table_names:
        for table_to in table_names:
            if table_from != table_to:
                tables.update(get_tables_in_path(table_from, table_to, collection_name))

    return tables
