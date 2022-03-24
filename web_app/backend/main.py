from fastapi import FastAPI
from fastapi.responses import JSONResponse
import meilisearch
from src.elastic.check_connection import connect_elasticsearch
from src.elastic.search import search_word

app = FastAPI()


@app.get("/")
async def main_page():
    status_data = {
        'connection to ElasticSearch': connect_elasticsearch(),
        'connection to Meili': False
    }
    return JSONResponse(content=status_data)

@app.get("/search/elastic/")
async def read_item(query: str):
    search_data = search_word(query)
    return JSONResponse(content=search_data)


@app.get("/search/meilis/")
async def read_item(query: str):
    client = meilisearch.Client('http://0.0.0.0:7700')
    
    search_data = client.index('movies').search(query)
    return JSONResponse(content=search_data)

