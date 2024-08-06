from fastapi import FastAPI
from app.api.endpoints import chat

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["items"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
