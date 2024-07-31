from operator import itemgetter

from langchain_community.vectorstores.qdrant import Qdrant
from langchain_core.language_models import BaseChatModel
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import Runnable
from app.templates.sql_prompt import _sqlite_prompt


def _process_and_print_docs(docs):
    print([doc.page_content for doc in docs])
    return "\n".join([doc.page_content for doc in docs])


def create_chain(
        chat_llm: BaseChatModel,
        vector_store: Qdrant,
        k_tables: int,
        k_nouns: int,
) -> Runnable:
    proper_nouns_retriever = vector_store.as_retriever(
        search_kwargs={"filter": {"type": "proper_noun"},
                       "k": k_tables})

    table_info_retriever = vector_store.as_retriever(
        search_kwargs={"filter": {"type": "table"},
                       "k": k_nouns})

    prompt = ChatPromptTemplate.from_messages([("system", _sqlite_prompt), ("human", "{input}")])

    response_generator = prompt | chat_llm | StrOutputParser()

    chain = (
            {
                "table_info": itemgetter("question") | table_info_retriever | _process_and_print_docs,
                "proper_nouns": itemgetter("question") | proper_nouns_retriever | _process_and_print_docs,
                "input": itemgetter("question")}
            | response_generator
    )
    return chain
