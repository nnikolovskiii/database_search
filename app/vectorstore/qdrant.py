from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Qdrant
from qdrant_client import QdrantClient

client = QdrantClient(url="http://localhost:6333")


def get_qdrant_vectorstore(
        collection_name: str,
        embeddings: Embeddings,
        client: QdrantClient = client,
) -> Qdrant:
    qdrant = Qdrant(client, collection_name, embeddings)
    return qdrant
