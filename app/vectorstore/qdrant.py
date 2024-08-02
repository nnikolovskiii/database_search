from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient, models

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


def search_embeddings(query: str, collection_name: str = "database_search", top_k: int = 5) -> List[Dict[str, Any]]:
    vector = embedd_content(query)

    search_result = client.search(
        collection_name=collection_name,
        query_vector=vector,
        limit=top_k
    )

    results = []
    for point in search_result:
        result = {
            "table_name": point.payload.get("table_name"),
            "column_name": point.payload.get("column_name"),
            "value": point.payload.get("value"),
            "score": point.score
        }
        results.append(result)

    return results


Query = "krstine23"
Results = search_embeddings(Query)

for r in Results:
    print(
        f"Table: {r['table_name']}, Column: {r['column_name']}, Value: {r['value']}, Score: {r['score']}")
