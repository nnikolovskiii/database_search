from fastapi import HTTPException
from app.chains.create_sql_query_chain import create_sql_query
from app.chains.sql_guardrail_chain import guardrail_chain
from fastapi import APIRouter

router = APIRouter()


@router.post("/{collection_name}")
def get_sql_query(collection_name: str, prompt: str):
    result = guardrail_chain(prompt)
    if result['verdict'] == "no":
        raise HTTPException(status_code=400, detail=result['reason'])
    response = create_sql_query(collection_name, prompt)

    return {"query": response}
