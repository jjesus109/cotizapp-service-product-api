from app.config import Config
from app.db import DBConnection
from app.utilities import get_token
from app.models import ServiceModel, ServiceUpdateModel

import uvicorn
import requests
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from fastapi import FastAPI, HTTPException, status

from pymongo.errors import (
    ConnectionFailure,
    ExecutionTimeout
)


conf = Config()
app = FastAPI()
db_conn = DBConnection(conf.mongodb_url)


@app.get("/api/v1/products")
async def search_product(category: str, brand: str, word_to_search: str):
    token = get_token()
    URL = f"{conf.syscom_api_url}?categoria={category}&marca={brand}&busqueda={word_to_search}"  # noqa
    autorization_header = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(URL, headers=autorization_header)
    return response


@app.get("/api/v1/services")
async def search_service_by_name(service_name: str):
    try:
        services_get = await db_conn.db["services"].find(
            {
                "name": {
                    "$regex": service_name,
                    "$options": "mxsi"
                    }
                }
        ).to_list(1000)
    except (ConnectionFailure, ExecutionTimeout):
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the service"
        )
    return services_get


@app.get("/api/v1/services/description")
async def search_service_by_description(service_description: str):
    try:
        services_get = await db_conn.db["services"].find(
            {
                "description": {
                    "$regex": service_description,
                    "$options": "mxsi"
                    }
                }
        ).to_list(1000)
    except (ConnectionFailure, ExecutionTimeout):
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the service description"
        )
    return services_get


@app.post(
        "/api/v1/services",
        response_description="Add new service",
        response_model=ServiceModel)
async def create_service(service: ServiceModel):
    service = jsonable_encoder(service)
    try:
        await db_conn.db["services"].insert_one(service)
    except (ConnectionFailure, ExecutionTimeout):
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not insert data problems with DB connection"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=service
    )


# reference:
# https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude_unset-parameter
@app.patch("/api/v1/services/{service_id}")
async def modify_service(service_id: int, service: ServiceUpdateModel):
    pass


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
