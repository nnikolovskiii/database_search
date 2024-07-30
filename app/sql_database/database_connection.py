from typing import List, Tuple

import psycopg2

from app.models.enums.postgres_data_types import PostgresDataType
from app.vectorstore.qdrant import upsert_record

db_config = {
    'dbname': 'sample-sql_database',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '9871'
}


def get_tables(
        table_schema: str = "public"
) -> List[str]:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = '{table_schema}';
    """)

    tables = cur.fetchall()

    cur.close()
    conn.close()

    return [table[0] for table in tables]


def get_columns_by_table(
        table_name: str
) -> List[Tuple[str, PostgresDataType]]:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
          AND table_schema = 'public';
    """)

    columns = cur.fetchall()

    cur.close()
    conn.close()

    return [(column_name, PostgresDataType(column_type)) for column_name, column_type in columns]
