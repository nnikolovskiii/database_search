from typing import List, Dict, Any
import uuid
from qdrant_client import QdrantClient, models

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

