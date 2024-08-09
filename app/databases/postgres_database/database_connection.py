from typing import List, Dict, Any, Optional, Tuple
import psycopg2
from psycopg2.extras import RealDictCursor
from pydantic import BaseModel
from dataclasses import dataclass
from contextlib import contextmanager

from app.models.enums.postgres_data_types import PostgresDataType
from app.models.outputs import SqlGenerationOutput
from app.templates.chat_output_template import chat_output_template


@dataclass(frozen=True)
class DatabaseConnection(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: str
    table_schema: str


DATABASE_CONNECTIONS = {}

database_initial = DatabaseConnection(
    dbname="sample-database",
    user="postgres",
    password="postgres",
    host="localhost",
    port="9871",
    table_schema="public"
)

DATABASE_CONNECTIONS[database_initial] = database_initial


@dataclass(frozen=True)
class Column(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    foreign_key_table: Optional[str]
    is_primary_key: bool = False

    def __str__(self):
        constraints = []
        if self.is_primary_key:
            constraints.append("PRIMARY KEY")
        if self.foreign_key_table != "None":
            constraints.append(f"FOREIGN KEY REFERENCES {self.foreign_key_table}")
        if not self.is_nullable:
            constraints.append("NOT NULL")

        return f"{self.name} {self.data_type} {' '.join(constraints)}".strip()


@dataclass(frozen=True)
class Table(BaseModel):
    name: str
    columns: Tuple[Column]

    def __str__(self):
        columns_str = "\n  ".join(str(column) for column in self.columns)
        return f"Table: {self.name}\n  {columns_str}"


@contextmanager
def get_db_connection(database: DatabaseConnection):
    conn = psycopg2.connect(
        dbname=database.dbname,
        user=database.user,
        password=database.password,
        host=database.host,
        port=database.port
    )
    try:
        yield conn
    finally:
        conn.close()


def fetch_all(cursor, query: str, params: Tuple = ()) -> List[Dict[str, Any]]:
    cursor.execute(query, params)
    return cursor.fetchall()


def get_tables_with_foreign_keys(database: DatabaseConnection) -> Dict[str, Any]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            tables = fetch_all(cur, """
                SELECT table_name FROM information_schema.tables WHERE table_schema = %s;
            """, (database.table_schema,))
            tables = [table['table_name'] for table in tables]

            all_foreign_keys = {}
            for table in tables:
                foreign_keys = fetch_all(cur, """
                    SELECT kcu.column_name, ccu.table_name AS foreign_table_name
                    FROM information_schema.table_constraints tc
                    JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                    JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
                    WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name = %s AND tc.table_schema = %s;
                """, (table, database.table_schema))

                all_foreign_keys[table] = foreign_keys or []

            return all_foreign_keys


def get_tables(database: DatabaseConnection) -> List[str]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            tables = fetch_all(cur, """
                SELECT table_name FROM information_schema.tables WHERE table_schema = %s;
            """, (database.table_schema,))
            return [table['table_name'] for table in tables]


def get_active_table_names():
    return list(["users", "categories", "products", "orders", "orderitems", "payments", "carts", "cartitems", "reviews",
                 "addresses", "paymentmethods", "shipments", "discounts", "shippingmethods", "shippingrates"
                 ])


def get_columns_by_table(database: DatabaseConnection, table_name: str) -> List[Column]:
    with get_db_connection(database) as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            columns = fetch_all(cur, """
                SELECT column_name, data_type, is_nullable FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s;
            """, (table_name, database.table_schema))

            primary_key_columns = fetch_all(cur, """
                SELECT a.attname AS column_name FROM pg_index i
                JOIN pg_attribute a ON a.attnum = ANY(i.indkey)
                WHERE i.indisprimary AND i.indrelid = %s::regclass;
            """, (table_name,))
            primary_key_columns = {col['column_name'] for col in primary_key_columns}

            foreign_keys = fetch_all(cur, """
                SELECT kcu.column_name, ccu.table_name AS foreign_table_name
                FROM information_schema.table_constraints tco
                JOIN information_schema.key_column_usage kcu ON kcu.constraint_name = tco.constraint_name
                JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tco.constraint_name
                WHERE tco.table_name = %s AND tco.constraint_type = 'FOREIGN KEY';
            """, (table_name,))
            foreign_keys_dict = {fk['column_name']: fk['foreign_table_name'] for fk in foreign_keys}

            return [
                Column(
                    name=col['column_name'],
                    data_type=PostgresDataType(col['data_type']),
                    is_nullable=(col['is_nullable'] == 'YES'),
                    is_primary_key=(col['column_name'] in primary_key_columns),
                    foreign_key_table=foreign_keys_dict.get(col['column_name'])
                ) for col in columns
            ]


def get_char_varchar_text_columns(database: DatabaseConnection, table_name: str) -> List[str]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            columns = fetch_all(cur, """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s AND data_type IN ('character varying', 'character', 'text');
            """, (table_name, database.table_schema))
            return [column['column_name'] for column in columns]


def get_column_values(database: DatabaseConnection, table_name: str, column_name: str) -> List[str]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            values = fetch_all(cur, f'SELECT "{column_name}" FROM "{table_name}";')
            return [value[column_name] for value in values if value[column_name] is not None]


def run_query(dbname: str, sql_output: SqlGenerationOutput) -> str:
    database = DATABASE_CONNECTIONS.get(dbname)

    if not database:
        raise ValueError(f"Database connection for '{dbname}' not found.")

    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            try:
                cur.execute(sql_output.query)
                results = cur.fetchall()
                conn.commit()
                return chat_output_template(
                    query=sql_output.query,
                    output=results
                )
            except Exception as e:
                conn.rollback()
                print(sql_output.reason)
                return str(e)
