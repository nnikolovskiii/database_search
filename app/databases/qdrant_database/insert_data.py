from app.databases.postgres_database.database_connection import (
    get_tables,
    get_columns_by_table,
    get_char_varchar_text_columns,
    get_column_values,
    DatabaseConnection
)
from app.openai.embedding import embedd_content
from app.databases.qdrant_database.qdrant import upsert_record, create_collection
from tqdm import tqdm


def embedd_table_names(database: DatabaseConnection):
    tables = get_tables(database)
    collection_name = database.dbname
    for table_name in tqdm(tables, desc="Embedding Table Names"):
        metadata = {"table_name": table_name}
        vector = embedd_content(table_name)
        upsert_record(vector, metadata, collection_name)


def embedd_columns(database: DatabaseConnection):
    tables = get_tables(database)
    collection_name = database.dbname
    for table_name in tqdm(tables, desc="Embedding Columns"):
        columns = get_columns_by_table(database, table_name)
        for column in columns:
            metadata = {
                "table_name": table_name,
                "column_name": column.name
            }
            vector = embedd_content(column.name)
            upsert_record(vector, metadata, collection_name)


def embedd_string_values(database: DatabaseConnection):
    tables = get_tables(database)
    collection_name = database.dbname
    for table_name in tqdm(tables, desc="Embedding String Values by Table"):
        char_varchar_text_columns = get_char_varchar_text_columns(database, table_name)
        for column_name in tqdm(char_varchar_text_columns, desc=f"Processing {table_name}", leave=False):
            column_values = get_column_values(database, table_name, column_name)
            for value in tqdm(column_values, desc=f"Embedding {column_name} Values", leave=False):
                metadata = {
                    "table_name": table_name,
                    "column_name": column_name,
                    "value": value
                }
                vector = embedd_content(value)
                upsert_record(vector, metadata, collection_name)


def embedd_database(database: DatabaseConnection, include_values: bool):
    create_collection(database.dbname)
    embedd_table_names(database)
    embedd_columns(database)
    if include_values:
        embedd_string_values(database)
