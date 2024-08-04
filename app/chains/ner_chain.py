from typing import List

from app.ner_prompt.ner_prompt import ner_prompt, trim_and_load_json
from app.openai.chat import chat_with_openai


def ner_chain(
        query: str
) -> List[str]:
    prompt = ner_prompt(text=query)
    output = chat_with_openai(message=prompt)
    extracted_info = trim_and_load_json(output)

    if not isinstance(extracted_info, dict) or "information" not in extracted_info:
        raise ValueError("Invalid extracted information format.")

    return extracted_info["information"]


print(ner_chain("I want you to give me all the users that bought coffee and milk. "
                "Then from them count the users who live in Macedonia."))
