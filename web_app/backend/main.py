import meilisearch
import uvicorn

from fastapi import FastAPI
from fastapi import BackgroundTasks
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.elastic.check_connection import connect_elasticsearch
from src.elastic.search import search_word
from src.elastic.es_make_data import main as es_data
from src.meili.meili_make_data import main as mei_data
from src.app_config.settings import get_main_ip


BACKEND_IP = get_main_ip()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Search service",
        description="Just my experements with serch systems and Fastapi",
        version="0.1",
    )

    @app.get("/health")
    async def health() -> str:
        return "ok"

    return app


app = create_app()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/statuses")
async def main_page():
    ip = get_main_ip()
    meili_server = meilisearch.Client(f"http://{ip}:7700", "nilsir")
    status_data = {
        "connection to ElasticSearch": connect_elasticsearch(),
        "connection to Meili": meili_server.is_healthy(),
    }
    return JSONResponse(content=status_data)


@app.get("/search/elastic/")
async def read_item(query: str):
    search_data = search_word(query, BACKEND_IP)
    return JSONResponse(content=search_data)


@app.get("/search/meilis/")
async def read_item(query: str):
    ip = get_main_ip()
    client = meilisearch.Client(f"http://{ip}:7700", "nilsir")
    search_data = client.index("movies").search(query)
    from datetime import datetime

    for i in range(len(search_data["hits"])):

        date = int(search_data["hits"][i]["release_date"])
        search_data["hits"][i]["release_date"] = str(
            datetime.utcfromtimestamp(date).strftime("%d.%m.%Y")
        )

    return JSONResponse(content=search_data)


@app.post("/load-data/{system}")
async def send_notification(system: str, background_tasks: BackgroundTasks):
    # TODO refactoring
    def load_data(system: str):
        match system:
            case "elastic":
                es_data(BACKEND_IP)
                JSONResponse(content={"status": "Ok", "system": system})
            case "meili":
                mei_data(BACKEND_IP)
                JSONResponse(content={"status": "Ok", "system": system})
            case "both":
                mei_data(BACKEND_IP)
                es_data(BACKEND_IP)
                JSONResponse(content={"status": "Ok", "system": "elastic & meili"})

    background_tasks.add_task(load_data, system)
    return {"message": "Notification sent in the background"}


def run_server():
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug",
        debug=True,
        # workers=1,
        # limit_concurrency=1,
        # limit_max_requests=1,
    )


if __name__ == "__main__":
    run_server()

# TODO cinfiguration class - set back ip for app
