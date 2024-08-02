from typing import Any, Dict

from neo4j import GraphDatabase
from pydantic import BaseModel

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Test09875"

driver = GraphDatabase.driver(uri, auth=(username, password))


class Node(BaseModel):
    type: str
    properties: Dict[str, Any]


class Relationship(BaseModel):
    type: str


def _transform_properties(properties: Dict[str, Any]) -> str:
    return ", ".join(f"{key}: '{value}'" for key, value in properties.items())


def create_node(node: Node):
    with driver.session() as session:
        properties = _transform_properties(node.properties)
        cypher_query = f"CREATE (n:{node.type} {{{properties}}}) RETURN n"
        session.run(cypher_query)


def node_exists(node: Node) -> bool:
    with driver.session() as session:
        label = node.type
        label_existence_query = f"CALL db.labels() YIELD label RETURN label"
        labels_result = session.run(label_existence_query)
        labels = [record["label"] for record in labels_result]

        if label not in labels:
            return False

        properties = _transform_properties(node.properties)
        cypher_query = f"MATCH (n:{label} {{{properties}}}) RETURN n"
        result = session.run(cypher_query)
        return result.single() is not None


def create_relationship(node1: Node, node2: Node, relationship: Relationship):
    if not node_exists(node1):
        create_node(node1)
    if not node_exists(node2):
        create_node(node2)

    with driver.session() as session:
        properties1 = _transform_properties(node1.properties)
        properties2 = _transform_properties(node2.properties)
        cypher_query = f"""MATCH (node1:{node1.type} {{{properties1}}}), (node2:{node2.type} {{{properties2}}})
        CREATE (node1)-[:{relationship.type}]->(node2)"""
        session.run(cypher_query)
