from typing import List

from langchain_community.vectorstores.qdrant import Qdrant
from qdrant_client import QdrantClient
from sqlalchemy import create_engine, inspect


def upload_database_tables_to_vectorstore(
        url: str,
        qdrant: Qdrant,
) -> bool:
    """
    Uploads information about database tables and columns to a Qdrant vectorstore collection.

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

            # Add table information
            texts.append(table_name)
            metadatas.append({"type": "table"})

            # Add column information with details
            for column in table:
                column_name = column['name']
                texts.append(column_name)
                metadatas.append({
                    "type": "column",
                    "table": table_name,
                    "value_type": str(column['type']),
                })

        # Upload data to Qdrant
        qdrant.add_texts(texts=texts, metadatas=metadatas)
        return True

    except Exception as e:
        print(f"Error uploading database schema to Qdrant: {e}")
        return False
