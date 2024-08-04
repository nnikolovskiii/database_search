import json
from typing import Any, List

from app.openai.chat import chat_with_openai


def ner_prompt(text: str):
    return f"""
    You are an expert at extracting relevant information from text for searching in a SQL relational database.
    Your task is to identify all key concepts, nouns, verbs, and other elements that can help in searching for 
    table names, column names, and string values. Ensure to extract information that is directly useful for database
    queries.

    Example 1:
    Input:
    What are the top 3 products purchased by John Doe?

    Output:
    {{ "information": ["products", "purchased", "John Doe"] }}

    Example 2:
    Input:
    List all employees who joined in 2020.

    Output:
    {{ "information": ["employees", "joined", "2020"] }}

    Example 3:
    Input:
    Find all orders placed in the last month.

    Output:
    {{ "information": ["orders", "placed", "last month"] }}

    Example 4:
    Input:
    Retrieve customer details for Jane Smith.

    Output:
    {{ "information": ["customer details", "Jane Smith"] }}

    Text:
    {text}

    Return the extracted information in a list in JSON format.
    """


# print(ner_prompt(text="How many users have pruchased a bear bottle minimum 10 times?"))


def trim_and_load_json(input_string: str) -> Any:
    start = input_string.find("{")
    end = input_string.rfind("}") + 1

    if end == 0 and start != -1:
        input_string = input_string + "}"
        end = len(input_string)

    json_str = input_string[start:end] if start != -1 and end != 0 else ""

    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        raise ValueError("The output is not a valid JSON.")
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")


def ner_chain(
        query: str
) -> List[str]:
    prompt = ner_prompt(text=query)
    output = chat_with_openai(message=prompt)
    extracted_info = trim_and_load_json(output)

    if not isinstance(extracted_info, dict) or "information" not in extracted_info:
        raise ValueError("Invalid extracted information format.")

    return extracted_info["information"]
