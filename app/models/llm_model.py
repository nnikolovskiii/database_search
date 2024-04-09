from langchain_community.utilities import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI

db = SQLDatabase.from_uri("sqlite:///C:/Users/Nikola/DataGripProjects/myFirstProject/identifier.sqlite", sample_rows_in_table_info=3)
# print(db.dialect)
# print(db.get_usable_table_names())
# print(db.run("SELECT * FROM Customer LIMIT 10;"))


llm = ChatOpenAI(model="gpt-3.5-turbo", temperature="0", openai_api_key = "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")
chain = create_sql_query_chain(llm, db)
# chain.get_prompts()[0].pretty_print()
context = db.get_context()
# print(list(context))
prompt_with_context = chain.get_prompts()[0].partial(table_info=context["table_info"])
print(prompt_with_context.pretty_repr()[:1500])

examples = [
    {"input": "List all artists.", "query": "SELECT * FROM Artist;"},
    {
        "input": "Find all albums for the artist 'AC/DC'.",
        "query": "SELECT * FROM Album WHERE ArtistId = (SELECT ArtistId FROM Artist WHERE Name = 'AC/DC');",
    },
    {
        "input": "List all tracks in the 'Rock' genre.",
        "query": "SELECT * FROM Track WHERE GenreId = (SELECT GenreId FROM Genre WHERE Name = 'Rock');",
    },
    {
        "input": "Find the total duration of all tracks.",
        "query": "SELECT SUM(Milliseconds) FROM Track;",
    },
    {
        "input": "List all customers from Canada.",
        "query": "SELECT * FROM Customer WHERE Country = 'Canada';",
    },
    {
        "input": "How many tracks are there in the album with ID 5?",
        "query": "SELECT COUNT(*) FROM Track WHERE AlbumId = 5;",
    },
    {
        "input": "Find the total number of invoices.",
        "query": "SELECT COUNT(*) FROM Invoice;",
    },
    {
        "input": "List all tracks that are longer than 5 minutes.",
        "query": "SELECT * FROM Track WHERE Milliseconds > 300000;",
    },
    {
        "input": "Who are the top 5 customers by total purchase?",
        "query": "SELECT CustomerId, SUM(Total) AS TotalPurchase FROM Invoice GROUP BY CustomerId ORDER BY TotalPurchase DESC LIMIT 5;",
    },
    {
        "input": "Which albums are from the year 2000?",
        "query": "SELECT * FROM Album WHERE strftime('%Y', ReleaseDate) = '2000';",
    },
    {
        "input": "How many employees are there",
        "query": 'SELECT COUNT(*) FROM "Employee"',
    },
]

from langchain_core.prompts import FewShotPromptTemplate, PromptTemplate


prompt = PromptTemplate.from_template("You are a SQLite expert. Given an input question, create a syntactically correct SQLite query to run.\n\nHere is the relevant table info: {table_info}\n\nBelow are a number of examples of questions and their corresponding SQL queries. \nUser input: {input}\nSQL query:")

prompt_with_context = prompt.partial(table_info=context["table_info"])

chain = prompt_with_context | llm

print(chain.invoke({"input": "List all artist that are in the genre jazz."}))


