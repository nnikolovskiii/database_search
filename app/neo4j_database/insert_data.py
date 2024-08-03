from typing import Tuple

from app.neo4j_database.neo4j_database import create_relationship, Node, Relationship
from app.sql_database.database_connection import get_tables_with_foreign_keys
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


def insert_tables_with_foreign_keys(

):
    tables = get_tables_with_foreign_keys()
    for table_name, foreign_keys in tables.items():
        fks = [ForeignKey(foreign_key) for foreign_key in foreign_keys]

        for fk in fks:
            create_relationship(
                node1=Node(
                    type="Table",
                    properties={"name": fk.to_table}
                ),
                node2=Node(
                    type="Table",
                    properties={"name": table_name}
                ),
                relationship=Relationship(type="FOREIGN_KEY")
            )


insert_tables_with_foreign_keys()
