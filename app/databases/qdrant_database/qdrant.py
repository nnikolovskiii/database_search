import json
from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient, models
import requests

from app.openai.embedding import embedd_content

client = QdrantClient(url="http://localhost:6333")


def create_collection(
        collection_name: str
):
    client.create_collection(
        collection_name=collection_name,
        vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
    )


def upsert_record(
        vector: List[float],
        metadata: Dict[str, Any],
        collection_name: str
) -> None:
    unique_id = str(uuid.uuid4())

    client.upsert(
        collection_name=collection_name,
        points=[
            models.PointStruct(
                id=unique_id,
                payload=metadata,
                vector=vector,
            ),
        ],
    )


def search_embeddings(
        query: str,
        search_type: str = None,
        collection_name: str = "database_search",
        top_k: int = 5
) -> List[Dict[str, Any]]:
    headers = {
        "Content-Type": "application/json"
    }

    filter_condition = None
    if search_type == "table_name":
        filter_condition = {
            "must": [
                {"is_empty": {"key": "column_name"}}
            ]
        }
    elif search_type == "column_name":
        filter_condition = {
            "must": [
                {"is_empty": {"key": "value"}},
            ],
            "must_not": [
                {"is_empty": {"key": "column_name"}}
            ]
        }
    elif search_type == "value":
        filter_condition = {
            "must_not": [
                {"is_empty": {"key": "value"}}
            ]
        }

    query_vector = embedd_content(query)

    payload = {
        "vector": query_vector,
        "limit": top_k,
        "with_payload": True,
        "filter": filter_condition,
        "score_threshold": 0.6
    }

    response = requests.post(
        f"http://localhost:6333/collections/{collection_name}/points/search",
        headers=headers,
        data=json.dumps(payload)
    )

    response.raise_for_status()
    search_result = response.json()

    results = []
    for point in search_result["result"]:
        result = {
            "table_name": point['payload'].get("table_name"),
            "column_name": point['payload'].get("column_name"),
            "value": point['payload'].get("value"),
            "score": point['score']
        }
        results.append(result)

    return results
