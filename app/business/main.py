import logging

from app.config import Config
from app.connections import create_connection, create_producer
from app.infrastructure.repository import Repository
from app.adapters.gateway import Gateway
from app.entities.models import (
    ServiceModel,
    ServiceUpdateModel,
    ProductModel
)

from app.errors import ElementNotFoundError

import uvicorn
from fastapi.responses import JSONResponse
from fastapi import FastAPI, HTTPException, status

conf = Config()
app = FastAPI()
log = logging.getLogger(__name__)
nosql_connection = create_connection()
messaging_conn = create_producer()
gateway = Gateway(
    Repository(
        nosql_connection,
        messaging_conn
    )
)


@app.get("/api/v1/products")
async def search_product(product_name: str):
    try:
        products = await gateway.search_product(product_name)
    except ElementNotFoundError as e:
        log.error(f"Could not get data from third party endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not get data from third party endpoint"
        )
    except Exception as e:
        log.error(f"Could not get data from third party endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not search the product"
        )
    return products


@app.get("/api/v1/services")
async def search_service_by_name(service_name: str):
    try:
        services = await gateway.search_services_by_name(service_name)
    except ElementNotFoundError as e:
        log.error(f"Could not find the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not finde the service"
        )
    except Exception as e:
        log.error(f"Could not find the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not search the service"
        )
    return services


@app.get("/api/v1/services/description")
async def search_service_by_description(service_description: str):
    try:
        services = await gateway.search_services_by_description(
            service_description
        )
    except ElementNotFoundError as e:
        log.error(f"Could not find the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the service"
        )
    except Exception as e:
        log.error(f"Could not find the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not search the service"
        )
    return services


@app.get("/api/v1/services/{service_id}")
async def get_service(service_id: str):
    try:
        service = await gateway.get_service(service_id)
    except ElementNotFoundError as e:
        log.error(f"Could not find the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the service"
        )
    except Exception as e:
        log.error(f"Could not find the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the service"
        )
    return service


@app.get("/api/v1/products/{product_id}")
async def get_product(product_id: str):
    try:
        product = await gateway.get_product(product_id)
    except ElementNotFoundError as e:
        log.error(f"Could not find the product: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the product"
        )
    except Exception as e:
        log.error(f"Could not find the product: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not find the product"
        )
    return product


@app.post(
        "/api/v1/services",
        response_description="Add new service",
        response_model=ServiceModel)
async def create_service(service: ServiceModel):
    try:
        service = await gateway.create_service(service)
    except ElementNotFoundError as e:
        log.error(f"Could not create the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could create the service"
        )
    except Exception as e:
        log.error(f"Could not create the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create the service"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=service
    )


@app.post(
        "/api/v1/products",
        response_description="Add new service",
        response_model=ProductModel)
async def create_product(product: ProductModel):
    try:
        product = await gateway.create_product(product)
    except ElementNotFoundError as e:
        log.error(f"Could not create the product: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could create the product"
        )
    except Exception as e:
        log.error(f"Could not create the product: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not create the product"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=product
    )


# reference:
# https://fastapi.tiangolo.com/tutorial/body-updates/#using-pydantics-exclude_unset-parameter
@app.patch("/api/v1/services/{service_id}")
async def modify_service(service_id: str, service: ServiceUpdateModel):
    try:
        service = await gateway.modify_service(service_id, service)
    except ElementNotFoundError as e:
        log.error(f"Could not update the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could update the service"
        )
    except Exception as e:
        log.error(f"Could not update the service: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Could not update the service"
        )
    return JSONResponse(
        status_code=status.HTTP_201_CREATED,
        content=service
    )


if __name__ == "__main__":
    uvicorn.run("main:app", port=5000, log_level="info")
