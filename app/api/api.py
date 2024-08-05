from fastapi import FastAPI, HTTPException

from app.chains.ner_chain import ner_chain
from app.chains.sql_guardrail_chain import guardrail_chain

app = FastAPI()


@app.post("/getQuery/")
def get_sql_query(prompt: str):
    result = guardrail_chain(prompt)
    if result['verdict'] == "no":
        raise HTTPException(status_code=400, detail=result['reason'])
    response = ner_chain(prompt)
    return {"query": response}
