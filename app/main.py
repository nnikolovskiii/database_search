from fastapi import FastAPI
from app.api.endpoints import chat
import uvicorn
import subprocess
import threading

from app.databases.postgres_database.database_connection import DatabaseConnection

app = FastAPI()

app.include_router(chat.router, prefix="/chat", tags=["items"])


def run_fastapi():
    print("Starting FastAPI...")
    uvicorn.run(app, host="0.0.0.0", port=8000)


def run_streamlit():
    try:
        print("Starting Streamlit...")
        subprocess.run(["streamlit", "run", "frontend/frontend.py", "--server.port", "8080"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Streamlit failed with error: {e}")


DATABASE_CONNECTIONS = {}

if __name__ == "__main__":
    database_initial = DatabaseConnection(
        dbname="sample-database",
        user="postgres",
        password="postgres",
        host="localhost",
        port="9871",
        table_schema="public"
    )

    DATABASE_CONNECTIONS[database_initial] = database_initial

    fastapi_thread = threading.Thread(target=run_fastapi)
    fastapi_thread.start()

    run_streamlit()
