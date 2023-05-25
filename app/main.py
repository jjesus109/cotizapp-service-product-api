from app.utilities import get_token
from app.models import ServiceModel, ServiceUpdateModel

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
    response = requests.get(URL, headers=autorization_header)
    return response


@app.get("/api/v1/services")
async def search_service(service: str):
    pass


@app.post("/api/v1/services")
async def create_service(service: ServiceModel):
    pass


# reference:
# https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude_unset-parameter
@app.patch("/api/v1/services/{service_id}")
async def modify_service(service_id: int, service: ServiceUpdateModel):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
