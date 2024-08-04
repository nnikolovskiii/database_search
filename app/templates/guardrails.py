def sql_query_guardrail(text: str):
    return f"""
    Given a question determine if the question could be transformed into a sql query.

    Example 1:
    Question: 
    How are you?
    
    {{
    "reason": "The question 'How are you?' is a conversational and open-ended question typically asked in social 
    interactions to inquire about someone's well-being. It does not relate to data retrieval, manipulation, or any 
    specific data-related operation that SQL is designed to handle.",
    "verdict": "no"
    }}
    
    Example 2:
    Question: 
    How many bear bottles are sold in 2023?

    {{
    "reason": "The question asks for the number of beer bottles sold in 2023. This can be addressed by querying a 
    database where sales data is stored, typically in a structured format such as SQL. The query would involve selecting
    and summing the quantity of beer bottles sold, filtered by the year 2023. Databases usually have tables that store 
    sales information with fields like product type, quantity, and date, making it feasible to construct a SQL query to 
    get the required information.",
    "verdict": "yes"
    }}
    
    {text}
    Return a json with key reason and verdict. First provide your reason why you think the question can or cannot be 
    transformed into sql. And in the end provide a  verdict yes if it could be transformed into sql query, and no if it 
    can not.
    """
