from langchain_openai import OpenAIEmbeddings

from app.database.database_connection import connect_database
from app.utils.database_schema_transfer import upload_database_tables_to_vectorstore
from app.vectorstore.qdrant import get_qdrant_vectorstore

url = "sqlite:///C:/Users/Nikola/DataGripProjects/myFirstProject/identifier.sqlite"
db = connect_database(url)
table_names = db.get_usable_table_names()
print(type(table_names))
print(table_names)

vdb = get_qdrant_vectorstore(collection_name="5e9ed7c960694b36938f3f252775efc9",
                             embeddings=OpenAIEmbeddings(
                                 openai_api_key="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"))

upload_database_tables_to_vectorstore(url=url, qdrant=vdb)

# query = "Artistic person and track and employee"
# docs = vdb.similarity_search(query, k=3)
# for i in range(3):
#     print(docs[i])
