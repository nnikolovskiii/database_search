from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI, OpenAIEmbeddings

from app.chains.main_chain import create_chain
from app.vectorstore.qdrant import get_qdrant_vectorstore

db = SQLDatabase.from_uri("sqlite:///C:/Users/Nikola/DataGripProjects/myFirstProject/identifier.sqlite", sample_rows_in_table_info=3)


chat_llm = ChatOpenAI(model="gpt-3.5-turbo", temperature="0", openai_api_key = "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")
context = db.get_context()
vdb = get_qdrant_vectorstore(collection_name="database_search",
                             embeddings=OpenAIEmbeddings(
                                 openai_api_key="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"))
# print(list(context))
chain = create_chain(chat_llm, vdb, 15, 5)
print(chain.invoke({"question": "List all customers that are Bjornis."}))


