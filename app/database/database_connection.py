from langchain_community.utilities import SQLDatabase

def connect_database(
        database_uri: str,
) -> SQLDatabase:
    db = SQLDatabase.from_uri(database_uri, sample_rows_in_table_info =0)
    return db
