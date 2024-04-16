from typing import List

from langchain_community.utilities import SQLDatabase
import ast
import re


def connect_database(
        database_uri: str,
) -> SQLDatabase:
    db = SQLDatabase.from_uri(database_uri, sample_rows_in_table_info=0)
    return db


def query_as_list(
        db: SQLDatabase,
        query: str
) -> List[str]:
    res = db.run(query)
    res = [el for sub in ast.literal_eval(res) for el in sub if el]
    res = [re.sub(r"\b\d+\b", "", string).strip() for string in res]
    return res
