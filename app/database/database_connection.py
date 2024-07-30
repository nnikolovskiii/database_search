from typing import List, Tuple

import psycopg2

db_config = {
    'dbname': 'sample-database',
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
) -> List[Tuple[str, str]]:
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

    return columns
