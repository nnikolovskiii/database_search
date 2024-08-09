from typing import Tuple
from app.databases.neo4j_database.neo4j_database import create_relationship, Node, Relationship, create_node
from app.databases.postgres_database.database_connection import get_tables_with_foreign_keys, get_tables, \
    get_columns_by_table, DatabaseConnection
from pydantic import BaseModel


class ForeignKey(BaseModel):
    from_column: str
    to_column: str
    to_table: str

    def __init__(self, data: Tuple[str]):
        super().__init__(
            from_column=data[0],
            to_column=data[1],
            to_table=data[2]
        )


def insert_tables_with_foreign_keys(database: DatabaseConnection):
    tables = get_tables_with_foreign_keys(database)
    for table_name, foreign_keys in tables.items():
        fks = [ForeignKey(foreign_key) for foreign_key in foreign_keys]

        for fk in fks:
            create_relationship(
                node1=Node(
                    type="Table",
                    properties={"name": fk.to_table, "collection_name": database.dbname}
                ),
                node2=Node(
                    type="Table",
                    properties={"name": table_name, "collection_name": database.dbname}
                ),
                relationship=Relationship(
                    type="FOREIGN_KEY",
                    properties=fk.model_dump()
                )
            )

            create_relationship(
                node1=Node(
                    type="Table",
                    properties={"name": table_name, "collection_name": database.dbname}
                ),
                node2=Node(
                    type="Table",
                    properties={"name": fk.to_table, "collection_name": database.dbname}
                ),
                relationship=Relationship(
                    type="REFERENCED_BY",
                    properties=fk.model_dump()
                )
            )

        if len(fks) == 0:
            create_node(
                node=Node(
                    type="Table",
                    properties={"name": table_name, "collection_name": database.dbname}
                )
            )


def insert_columns(database: DatabaseConnection):
    tables = get_tables(database)
    for table_name in tables:
        columns = get_columns_by_table(database, table_name)

        for column in columns:
            create_relationship(
                node1=Node(
                    type="Table",
                    properties={"name": table_name, "collection_name": database.dbname}
                ),
                node2=Node(
                    type="Column",
                    properties=column.model_dump()
                ),
                relationship=Relationship(
                    type="HAS_COLUMN",
                    properties=None
                )
            )
