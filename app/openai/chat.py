import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages.base import BaseMessage


def message_chat_llm(
        message: str
) -> BaseMessage:
    load_dotenv()
    openai_api_key = os.getenv("OPENAI_API_KEY")
    chat_llm = ChatOpenAI(
        model="gpt-3.5-turbo",
        temperature="0",
        openai_api_key = openai_api_key
    )

    return chat_llm.invoke(message)

print(message_chat_llm("How are you today?"))

