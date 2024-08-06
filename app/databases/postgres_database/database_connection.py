from typing import List, Dict, Any, Optional
import psycopg2
from pydantic import BaseModel
from app.models.enums.postgres_data_types import PostgresDataType
from psycopg2.extras import RealDictCursor

db_config = {
    'dbname': 'sample-database',
    'user': 'postgres',
    'password': 'postgres',
    'host': 'localhost',
    'port': '9871'
}


class Column(BaseModel):
    name: str
    data_type: str
    is_nullable: bool
    is_primary_key: bool = False
    foreign_key_table: Optional[str]

    def __str__(self):
        constraints = []
        if self.is_primary_key:
            constraints.append("PRIMARY KEY")
        if self.foreign_key_table != "None":
            constraints.append(f"FOREIGN KEY REFERENCES {self.foreign_key_table}")
        if not self.is_nullable:
            constraints.append("NOT NULL")

        constraints_str = " ".join(constraints)
        return f"{self.name} {self.data_type} {constraints_str}".strip()


class Table(BaseModel):
    name: str
    columns: List[Column]

    def __str__(self):
        columns_str = "\n  ".join(str(column) for column in self.columns)
        return f"Table: {self.name}\n  {columns_str}"


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
        else:
            all_foreign_keys[table] = []

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


def get_columns_by_table(table_name: str) -> List[Column]:
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor(cursor_factory=RealDictCursor)

    cur.execute("""
        SELECT 
            column_name,
            data_type,
            is_nullable
        FROM information_schema.columns
        WHERE table_name = %s
          AND table_schema = 'public';
    """, (table_name,))

    columns = cur.fetchall()

    cur.execute("""
        SELECT 
            a.attname AS column_name
        FROM 
            pg_index i
            JOIN pg_attribute a ON a.attnum = ANY(i.indkey)
            JOIN pg_class c ON c.oid = i.indrelid
            JOIN pg_namespace n ON n.oid = c.relnamespace
        WHERE 
            c.relname = %s 
            AND i.indisprimary;
    """, (table_name,))
    primary_key_columns = {row['column_name'] for row in cur.fetchall()}

    cur.execute("""
        SELECT 
            kcu.column_name,
            ccu.table_name AS foreign_table_name
        FROM 
            information_schema.table_constraints tco
            JOIN information_schema.key_column_usage kcu 
              ON kcu.constraint_name = tco.constraint_name
              AND kcu.constraint_schema = tco.constraint_schema
            JOIN information_schema.constraint_column_usage ccu
              ON ccu.constraint_name = tco.constraint_name
              AND ccu.constraint_schema = tco.constraint_schema
        WHERE 
            tco.table_name = %s 
            AND tco.constraint_type = 'FOREIGN KEY';
    """, (table_name,))
    foreign_keys = {row['column_name']: row['foreign_table_name'] for row in cur.fetchall()}

    cur.close()
    conn.close()

    return [
        Column(
            name=col['column_name'],
            data_type=PostgresDataType(col['data_type']),
            is_nullable=(col['is_nullable'] == 'YES'),
            is_primary_key=(col['column_name'] in primary_key_columns),
            foreign_key_table=foreign_keys.get(col['column_name'])
        ) for col in columns
    ]


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
