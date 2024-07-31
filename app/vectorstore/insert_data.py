from app.openai.embedding import embedd_content
from app.sql_database.database_connection import *
from app.vectorstore.qdrant import upsert_record


def embedd_table_names():
    tables = get_active_table_names()
    for table in tables:
        table_name = table
        metadata = {
            "table_name": table_name
        }

        vector = embedd_content(table_name)
        upsert_record(vector, metadata, "database_search")


def embedd_columns():
    tables = get_active_table_names()
    for table in tables:
        table_name = table
        columns = get_columns_by_table(table_name)

        for column in columns:
            column_name = column[0]

            metadata = {
                "table_name": table_name,
                "column_name": column_name
            }

            vector = embedd_content(column_name)

            upsert_record(vector, metadata, "database_search")


def embedd_string_values():
    tables = get_tables()
    for table in tables:
        table_name = table
        char_varchar_text_columns = get_char_varchar_text_columns(table_name)

        for column_name in char_varchar_text_columns:

            column_values = get_column_values(table_name, column_name)

            for value in column_values:
                metadata = {
                    "table_name": table_name,
                    "column_name": column_name,
                    "value": value
                }
                vector = embedd_content(value)

                upsert_record(vector, metadata, "database_search")


embedd_string_values()
embedd_table_names()
embedd_columns()
