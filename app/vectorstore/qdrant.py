from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient, models
from qdrant_client.http.models import ScoredPoint

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


def search_embeddings(query: str, search_type: str, collection_name: str = "database_search", top_k: int = 3) \
        -> list[ScoredPoint]:
    if search_type == "table_name":
        filter_condition = models.Filter(
            must=[
                models.FieldCondition(
                    key="column_name",
                    match=models.MatchValue(value="")
                )
            ]
        )

    elif search_type == "column_name":
        filter_condition = models.Filter(
            must_not=[
                models.FieldCondition(
                    key="column_name",
                    match=models.MatchValue(value="")
                )
            ],
            must=[
                models.FieldCondition(
                    key="value",
                    match=models.MatchValue(value="")
                )
            ]
        )
    elif search_type == "value":
        filter_condition = models.Filter(
            must_not=[
                models.FieldCondition(
                    key="value",
                    match=models.MatchValue(value="")
                )
            ]
        )

    else:
        raise ValueError("Invalid search type. Must be 'table', 'column', or 'value'.")
    vector = embedd_content(query)

    search_result = client.search(
        collection_name=collection_name,
        limit=top_k,
        query_vector=vector,
        scroll_filter=filter_condition,
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

    return search_result


Results = search_embeddings("How many users have pruchased a bear bottle minimum 10 times?", "value")

for r in Results:
    print(
        f"Table: {r['table_name']}, Column: {r['column_name']}, Value: {r['value']}, Score: {r['score']}")
