from datetime import datetime
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


def create_chain(retriever):
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful documentation Q&A assistant, trained to answer questions from LangSmith's documentation. LangChain is a framework for building applications using large language models."
                   f"\nThe current time is {datetime.now()}.\n\nRelevant documents will be retrieved in the following messages."),
        ("system", "{context}"),
        ("human", "{question}"),
    ])

    model = ChatOpenAI(model="gpt-3.5-turbo-16k", temperature=0)
    response_generator = prompt | model | StrOutputParser()

    chain = (
        {
            "relevant_tables": itemgetter("question") | retriever | (lambda docs: "\n".join([doc.page_content for doc in docs])),
            "relevant_columns": itemgetter("question") | retriever | (lambda docs: "\n".join([doc.page_content for doc in docs])),
            "question": itemgetter("question"),
        }
        | response_generator
    )
    return chain,