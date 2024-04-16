from typing import List

from langchain_community.utilities.sql_database import SQLDatabase
from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from sqlalchemy import create_engine, inspect

from app.database.database_connection import query_as_list

TEXT_TYPE_COLUMNS = ["CHARACTER", "VARCHAR", "VARYING CHARACTER", "NCHAR", "NATIVE CHARACTER", "NVARCHAR", "TEXT",
                     "CLOB"]


def _is_text_column_type(column_type):
    if str(column_type).split("(")[0] in TEXT_TYPE_COLUMNS:
        return True
    return False


def _create_select(
        column_name: str,
        table_name: str):
    return f"SELECT {column_name} FROM {table_name}"


def upload_database_tables_to_vectorstore(
        url: str,
        qdrant: Qdrant,
        db: SQLDatabase
) -> bool:
    """
    Uploads information about database tables, columns and proper nouns to a Qdrant vectorstore collection.

    Args:
        url (str): The connection URL for the database.
        qdrant (Qdrant): A Qdrant client object.

    Returns:
        bool: True if upload was successful, False otherwise.
    """

    try:
        engine = create_engine(url)
        inspector = inspect(engine)
        tables = inspector.get_table_names()

        # Prepare data structures for texts and metadatas
        texts: List[str] = []
        metadatas: List[dict] = []

        for table_name in tables:
            table = inspector.get_columns(table_name)
            db_table_info = db.get_table_info([table_name])

            # Add table information
            texts.append(table_name)
            metadatas.append({
                "type": "table",
                "table_info": db_table_info,
            })

            # Add column information with details
            for column in table:
                column_name = column['name']
                column_type = column['type']
                # texts.append(column_name)
                # metadatas.append({
                #     "type": "column",
                #     "table": table_name,
                #     "value_type": str(column['type']),
                # })

                if _is_text_column_type(column_type):
                    proper_nouns = query_as_list(db, _create_select(column_name, table_name))
                    for noun in proper_nouns:
                        texts.append(noun)
                        metadatas.append({
                            "type": "proper_noun",
                            "table": table_name,
                            "column": column_name,
                        })

        # Upload data to Qdrant
        qdrant.add_texts(texts=texts, metadatas=metadatas)
        return True

    except Exception as e:
        print(f"Error uploading database schema to Qdrant: {e}")
        return False
