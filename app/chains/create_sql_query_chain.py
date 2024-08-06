def create_query(query: str):
    entities = ner_chain(query)
    tables, columns, values = [], [], []

    for elem in entities:
        tables.extend(search_embeddings(query=elem, search_type="table_name"))
        columns.extend(search_embeddings(query=elem, search_type="column_name"))
        values.extend(search_embeddings(query=elem, search_type="value"))

    table_names: List[str] = [table["table_name"] for table in tables] + [col["table_name"] for col in columns]
    values: List[str] = [value["value"] for value in values]

    tables: List[Table] = []

    for table_from in table_names:
        for table_to in table_names:
            if table_from != table_to:
                tables.extend(get_tables_in_path(table_from, table_to))

    table_info = "\n".join([str(table) for table in tables])
    proper_nouns = ", ".join([f"{v['value']}" for v in values])

    sql_query = postgresql_template(table_info, proper_nouns, query)
    return chat_with_openai(sql_query)