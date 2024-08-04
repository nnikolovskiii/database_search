from typing import List

from app.ner_prompt.ner_prompt import ner_prompt, trim_and_load_json
from app.openai.chat import chat_with_openai
from app.templates.guardrails import sql_query_guardrail


def ner_chain(
        query: str
) -> List[str]:
    prompt = sql_query_guardrail(text=query)
    output = chat_with_openai(message=prompt)
    extracted_info = trim_and_load_json(output)

    if not isinstance(extracted_info, dict) or "verdict" not in extracted_info:
        raise ValueError("Invalid extracted verdict format.")

    return extracted_info["verdict"]


# print(ner_chain(""))
