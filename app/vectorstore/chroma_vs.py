from typing import List
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings



#Test local vectorstore
def create_chroma_vectorstore(
    documents: List[Document]
) -> Chroma:
    db = Chroma.from_documents(documents, OpenAIEmbeddings(openai_api_key = "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"))
    return db

