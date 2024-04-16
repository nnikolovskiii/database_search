from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient, models

client = QdrantClient(url="http://localhost:6333")


def get_qdrant_vectorstore(
        collection_name: str,
        embeddings: Embeddings,
        client: QdrantClient = client,
) -> Qdrant:
    qdrant = Qdrant(client, collection_name, embeddings)
    return qdrant


def add_collection(
        collection_name: str,
        embeddings: Embeddings,
        client: QdrantClient = client,

) -> Qdrant:
    client.create_collection(collection_name=collection_name,
                             vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE),
                             )
    qdrant = Qdrant(client=client, collection_name=collection_name, embeddings=embeddings)
    print(qdrant.collection_name)
    return qdrant
