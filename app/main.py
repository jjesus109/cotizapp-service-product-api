from app.utilities import get_token

from fastapi import FastAPI
import requests
import uvicorn


app = FastAPI()
BASE_URL = "https://developers.syscom.mx/api/v1/"


@app.get("/api/v1/products")
async def search_product(category: str, brand: str, word_to_search: str):
    token = get_token()
    URL = f"{BASE_URL}?categoria={category}&marca={brand}&busqueda={word_to_search}"  # noqa
    autorization_header = {
        "Authorization": f"Bearer {token}"
    }
    requests.get(URL, headers=autorization_header)


@app.get("/")
async def get_product():
    return "Hi, man"


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
