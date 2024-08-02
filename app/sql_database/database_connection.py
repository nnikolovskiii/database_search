from typing import List, Tuple, Dict, Any
import psycopg2

from app.models.enums.postgres_data_types import PostgresDataType

db_config = {
    'dbname': 'sample-database',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '9871'
}


def get_tables_with_foreign_keys(
        table_schema: str = "public"
) -> Dict[str, Any]:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s;
    """, (table_schema,))
    tables = cur.fetchall()
    tables = [table[0] for table in tables]

    all_foreign_keys = {}

    for table in tables:
        cur.execute("""
            SELECT
                tc.constraint_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name
            FROM 
                information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu 
                  ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY' 
              AND tc.table_name = %s
              AND tc.table_schema = %s;
        """, (table, table_schema))

        foreign_keys = cur.fetchall()

        if foreign_keys:
            all_foreign_keys[table] = foreign_keys

    cur.close()
    conn.close()

    return all_foreign_keys


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