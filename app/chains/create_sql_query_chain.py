from typing import List, Set
from app.chains.ner_chain import ner_chain
from app.chains.validate_info_chain import validate_info_chain
from app.databases.neo4j_database.neo4j_database import get_tables_in_path
from app.openai.chat import chat_with_openai
from app.databases.postgres_database.database_connection import Table
from app.templates.create_sql_prompt import postgresql_template
from app.databases.qdrant_database.qdrant import search_embeddings, SearchOutput


def create_sql_query(query: str):
    entities = ner_chain(query)
    tables_objs: List[SearchOutput] = []
    columns_objs: List[SearchOutput] = []
    values_objs: List[SearchOutput] = []

    for elem in entities:
        tables_objs.extend(search_embeddings(query=elem, search_type="table_name", score_threshold=0.2, top_k=3))
        columns_objs.extend(search_embeddings(query=elem, search_type="column_name", score_threshold=0.2, top_k=3))
        values_objs.extend(search_embeddings(query=elem, search_type="value", score_threshold=0.8, top_k=3))

    tables = _get_tables_in_paths({table.table_name for table in tables_objs} | {col.table_name for col in columns_objs})
    table_info = "\n".join([str(table) for table in tables])

    validation_output = validate_info_chain(table_info=table_info, question=query)

    if validation_output.verdict == "no":
        missing_tables_objs: Set[SearchOutput] = set()

        for table in validation_output.missing_tables:
            missing_tables_objs.update(
                search_embeddings(
                    query=table,
                    search_type="table_name",
                    score_threshold=0.2)
            )

        missing_tables = _get_tables_in_paths({table.table_name for table in missing_tables_objs})
        tables.update(missing_tables)

    table_info = "\n".join([table.__str__() for table in tables])
    proper_nouns = ", ".join([value.value for value in values_objs])

    sql_query = postgresql_template(table_info, proper_nouns, query)
    return chat_with_openai(sql_query)


def _sort_search_outputs_by_score(search_outputs: Set[SearchOutput]) -> List[SearchOutput]:
    return sorted(search_outputs, key=lambda x: x.score, reverse=True)[:8]


def _get_tables_in_paths(
        table_names: Set[str],
) -> Set[Table]:
    tables: Set[Table] = set()
    for table_from in table_names:
        for table_to in table_names:
            if table_from != table_to:
                tables.update(get_tables_in_path(table_from, table_to))

    return tables
