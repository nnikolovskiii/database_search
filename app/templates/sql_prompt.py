def postgresql_template(
        table_info: str,
        proper_nouns: str,
        query: str
) -> str:
    return f"""You are a Postgres expert. Given an input question, create a syntactically correct SQLite query to run.
    Never query for all columns from a table. You must query only the columns that are needed to answer the question. Wrap each column name in double quotes (") to denote them as delimited identifiers.
    Pay attention to use only the column names you can see in the tables below. Be careful to not query for columns that do not exist. Also, pay attention to which column is in which table.
    Pay attention to use date('now') function to get the current date, if the question involves "today".
    
    Here is the relevant table info: 
    {table_info}
    
    Here is a non-exhaustive list of possible feature values. If filtering on a feature value make sure to check its spelling
    against this list first:
    {proper_nouns}
    
    Query:
    {query}
    """


print(postgresql_template(table_info="Sports, Orders, Categories", proper_nouns="Tennis, Volleyball"))
