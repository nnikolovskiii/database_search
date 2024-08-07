from fastapi import FastAPI
from app.api.endpoints import chat
import uvicorn
import subprocess
import threading

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["items"])


def run_fastapi():
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_streamlit():
    subprocess.run(["streamlit", "run", "frontend\\frontend.py"])


if __name__ == "__main__":
    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    run_streamlit()
