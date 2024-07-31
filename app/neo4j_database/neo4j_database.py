from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
username = "neo4j"
password = "Test09875"

driver = GraphDatabase.driver(uri, auth=(username, password))

def run_query(driver, query):
    with driver.session() as session:
        result = session.run(query)
        return list(result) 

query = "MATCH (n) RETURN n"

result = run_query(driver, query)
for record in result:
    print(record)

driver.close()
