from app.openai.chat import chat_with_openai


def ner_prompt(
    text: str
):
    return f"""Given the text bellow extract all relevant infomation that could be important for searching for columns, tables and string values in SQL realtional database. Extract every information that is useful. Include concepts, nouns, verbs that help search table names, column names and string values.

Example:
What top 3 products does nnikolovskii buy?

Output:
{{ "infomration": ["nnikolovskii","products"] }}


Text:
{text}

Return them in a list in json.
"""

print(ner_prompt(text="How many users have pruchased a bear bottle minimum 10 times?"))


def ner_chain(
        query: str
) -> List[str]:
    prompt = ner_prompt(text=query)
    output = chat_with_openai(message=prompt)
    extract_json(output)

    return Liust

for elem in list:
    type = ""
    list_elem = search_qdrant(elem, top_k=3, filter="column") # table i column, i nema value
    list_elem = search_qdrant(elem, top_k=3, filter="table") # table key i nema colona i nema value
    list_elem = search_qdrant(elem, top_k=3, filter="string_value")# value

    get_neighbouring_tables_neo4j()







def trimAndLoadJson(
    input_string: str, metric: Optional[BaseMetric] = None
) -> Any:
    start = input_string.find("{")
    end = input_string.rfind("}") + 1

    if end == 0 and start != -1:
        input_string = input_string + "}"
        end = len(input_string)

    jsonStr = input_string[start:end] if start != -1 and end != 0 else ""

    try:
        return json.loads(jsonStr)
    except json.JSONDecodeError:
        error_str = "Evaluation LLM outputted an invalid JSON. Please use a better evaluation model."
        if metric is not None:
            metric.error = error_str
        raise ValueError(error_str)
    except Exception as e:
        raise Exception(f"An unexpected error occurred: {str(e)}")