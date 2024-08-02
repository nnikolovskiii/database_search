from typing import List, Tuple

import psycopg2

from app.models.enums.postgres_data_types import PostgresDataType

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


def get_active_table_names():
    return list(["users", "categories", "products", "orders", "orderitems", "payments", "carts", "cartitems", "reviews",
                 "addresses", "paymentmethods", "shipments", "discounts", "shippingmethods", "shippingrates"
                 ])


def get_char_varchar_text_columns(table_name: str) -> List[str]:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = '{table_name}'
          AND table_schema = 'public'
          AND data_type IN ('character varying', 'character', 'text');
    """)

    columns = cur.fetchall()

    cur.close()
    conn.close()

    return [column[0] for column in columns]


def get_column_values(table_name: str, column_name: str) -> List[str]:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT "{column_name}"
        FROM "{table_name}";
    """)

    values = cur.fetchall()

    cur.close()
    conn.close()

    return [value[0] for value in values if value[0] is not None]
