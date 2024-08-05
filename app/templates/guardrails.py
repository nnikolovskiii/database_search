def sql_query_guardrail(text: str):
    return f"""
    You are an expert at extracting relevant information from text for searching in a SQL relational database.
    Your task is to identify all key concepts, nouns, verbs, and other elements that can help in searching for 
    table names, column names, and string values. Ensure to extract information that is directly useful for database
    queries.

    Example 1:
    Input:
    Firstly, give me all cars that have the brand Mercedes. From them extract the top 10 models that have the highest revenue from consumers. Sum up all of the revenue and return it to me.

    Output:
   {{"information": ["cars", "brand", "Mercedes", "models", "revenue", "consumers"]}}


    Example 2:
    Input:
    Show the inventory levels of all warehouses with a capacity greater than 1000 units.

    Output:
    {{ "information": ["inventory levels", "warehouses", "capacity", "units"] }}

    Example 3:
    Input:
    List all transactions involving customers who have a loyalty score above 80.

    Output:
    {{ "information": ["transactions", "customers", "loyalty score"] }}

    Example 4:
    Input:
    I want you to give me all the items that are bought buy the user John Doe. 
    Than from them find the highest priced item. 
    I want you return all the number of items that have that specific price.

    Output:
    {{ "information": ["items", "bought", "user", "John Doe", "price"] }}

    Text:
    Firstly, give me all cars that have the brand Mercedes. From them extract the top 10 models that have the highest revenue from consumers. Sum up all of the revenue and return it to me.

    Return the extracted information in a list in JSON format.
    """
