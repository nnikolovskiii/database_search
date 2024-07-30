import os
from typing import List
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings


def embedd_content(
        content: str
) -> List[float]:
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")

    if not openai_api_key:
        raise ValueError("OpenAI API key not found. Please set it in the .env file.")

    embedding_model = OpenAIEmbeddings(api_key=openai_api_key, model="text-embedding-3-small")
    vector = embedding_model.embed_query(content)
    return vector
