from datetime import datetime
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
class Database(BaseModel):
    dbname: str
    user: str
    password: str
    host: str
    port: int
    table_schema: Optional[str] = None
    date_created: Optional[datetime] = None


metadata_db_connection_info = Database(
    dbname='database_search_db',
    user='postgres',
    password='postgres',
    host='localhost',
    port=5433,
    table_schema=None,
    date_created=None,
)


def get_database_info_by_name(dbname: str) -> Optional[Database]:
    query = """
    SELECT * FROM database WHERE dbname = %s;
    """

    with get_db_connection(metadata_db_connection_info) as conn:
        with conn.cursor() as cur:
            cur.execute(query, (dbname,))
            result = cur.fetchone()

            if result:
                return Database(
                    dbname=result[0],
                    user=result[1],
                    password=result[2],
                    host=result[3],
                    port=result[4],
                    table_schema=result[5],
                    date_created=result[6]
                )
            else:
                return None


@dataclass(frozen=True)
class Column(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    collection_name: str
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
    columns: Tuple[Column, ...]

    def __str__(self):
        columns_str = "\n  ".join(str(column) for column in self.columns)
        return f"Table: {self.name}\n  {columns_str}"


@contextmanager
def get_db_connection(database: Database):
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


def register_database(database: Database):
    try:
        with get_db_connection(metadata_db_connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                       INSERT INTO "database" (host, port, "user", password, dbname, "schema", date_created)
                       VALUES (%s, %s, %s, %s, %s, %s, %s)
                   """, (
                    database.host,
                    database.port,
                    database.user,
                    database.password,
                    database.dbname,
                    database.table_schema,
                    datetime.now()
                ))
                conn.commit()
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()


def get_all_registered_databases():
    try:
        with get_db_connection(metadata_db_connection_info) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT dbname FROM "database"
                """)
                dbnames = [row[0] for row in cur.fetchall()]
                return dbnames
    except psycopg2.Error as e:
        print(f"Error: {e}")
        conn.rollback()
        return []


def fetch_all(cursor, query: str, params: Tuple = ()) -> List[Dict[Any, Any]]:
    cursor.execute(query, params)
    return cursor.fetchall()


def get_tables_with_foreign_keys(
        database: Database
) -> Dict[str, Any]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = %s;
            """, (database.table_schema,))

            tables = cur.fetchall()
            tables_names = [table[0] for table in tables]

            all_foreign_keys = {}

            for table in tables_names:
                cur.execute("""
                SELECT 
                tc.constraint_name, 
                kcu.column_name, 
                ccu.table_name AS foreign_table_name
                FROM information_schema.table_constraints AS tc 
                JOIN information_schema.key_column_usage AS kcu
                ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage AS ccu 
                ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' 
                AND tc.table_name = %s
                AND tc.table_schema = %s;
                """, (table, database.table_schema))

                foreign_keys = cur.fetchall()

                if foreign_keys:
                    all_foreign_keys[table] = foreign_keys
                else:
                    all_foreign_keys[table] = []

        cur.close()
        conn.close()

    return all_foreign_keys


def get_tables(database: Database) -> List[str]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            tables = fetch_all(cur, """
                SELECT table_name FROM information_schema.tables WHERE table_schema = %s;
            """, (database.table_schema,))
            return [table[0] for table in tables]


def get_active_table_names():
    return list(["users", "categories", "products", "orders", "orderitems", "payments", "carts", "cartitems", "reviews",
                 "addresses", "paymentmethods", "shipments", "discounts", "shippingmethods", "shippingrates"
                 ])


def get_columns_by_table(database: Database, table_name: str) -> List[Column]:
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


def get_char_varchar_text_columns(database: Database, table_name: str) -> List[str]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            columns = fetch_all(cur, """
                SELECT column_name FROM information_schema.columns
                WHERE table_name = %s AND table_schema = %s AND data_type IN ('character varying', 'character', 'text');
            """, (table_name, database.table_schema))
            return [column['column_name'] for column in columns]


def get_column_values(database: Database, table_name: str, column_name: str) -> List[str]:
    with get_db_connection(database) as conn:
        with conn.cursor() as cur:
            values = fetch_all(cur, f'SELECT "{column_name}" FROM "{table_name}";')
            return [value[column_name] for value in values if value[column_name] is not None]


def run_query(dbname: str, sql_output: SqlGenerationOutput) -> str:
    database = get_database_info_by_name(dbname)
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
