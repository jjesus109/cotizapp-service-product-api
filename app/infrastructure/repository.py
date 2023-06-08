import logging
from typing import List, Union
from dataclasses import dataclass

from app.config import Config
from app.errors import (
    ElementNotFoundError,
    TokenError,
    InsertionError,
    DBConnectionError
)
from app.entities.models import (
    ServiceModel,
    ServiceUpdateModel,
    ProductResponseSearchModel,
    ProductModel,
    ProducDictModel,
    ServiceDictModel,
    MessageFormat,
    MessageType
)
from app.infrastructure.repository_i import RepositoryInterface

import requests
from pydantic import BaseSettings
from confluent_kafka import Producer
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    ExecutionTimeout
)


log = logging.getLogger(__name__)
EMPTY_COUNT = 0


@dataclass
class Repository(RepositoryInterface):

    nosql_conn: AsyncIOMotorDatabase
    messaging_con: Producer
    config: BaseSettings = Config()

    async def get_service_data(self, service_id: int) -> ServiceDictModel:
        try:
            service = await self.nosql_conn["services"].find(
                {"_id": service_id}
            ).to_list(self.config.max_search_elements)
        except (ConnectionFailure, ExecutionTimeout):
            raise DBConnectionError(
                "Service not found in DB"
            )
        if service.__len__() == EMPTY_COUNT:
            raise ElementNotFoundError(
                "Service not found in DB"
            )
        return service[0]

    async def get_product_data(self, product_id: int) -> ProducDictModel:
        try:
            product = await self.nosql_conn["products"].find(
                {"_id": product_id}
            ).to_list(self.config.max_search_elements)
        except (DBConnectionError, ExecutionTimeout):
            raise ElementNotFoundError(
                "Service not found in DB"
            )
        if product.__len__() == EMPTY_COUNT:
            raise ElementNotFoundError(
                "Service not found in DB"
            )
        return product[0]

    async def search_products(
        self,
        word: str
    ) -> List[ProductResponseSearchModel]:
        token = await self._get_token()
        URL = f"{self.config.syscom_api_url}productos?busqueda={word}"
        autorization_header = {
            "Authorization": f"Bearer {token}"
        }
        try:
            response = requests.get(URL, headers=autorization_header)
            response.raise_for_status()
        except (
            requests.ConnectionError,
            requests.exceptions.ConnectTimeout
        ) as e:
            log.error(f"Could not get data from third party endpoint: {e}")
            raise ElementNotFoundError("Could not get product search data")
        raw_data = response.json()
        return raw_data.get("productos")

    async def search_services_by_name(
        self,
        service_name: str
    ) -> List[ServiceDictModel]:
        try:
            services_get = await self.nosql_conn["services"].find(
                {
                    "name": {
                        "$regex": service_name,
                        "$options": "mxsi"
                    }
                }
            ).to_list(self.config.max_search_elements)
        except (ConnectionFailure, ExecutionTimeout):
            raise DBConnectionError(
                "Could not found service in DB"
            )
        return services_get

    async def search_services_by_description(
        self,
        service_description: str
    ) -> List[ServiceDictModel]:
        try:
            services_get = await self.nosql_conn["services"].find(
                {
                    "description": {
                        "$regex": service_description,
                        "$options": "mxsi"
                    }
                }
            ).to_list(self.config.max_search_elements)
        except (ConnectionFailure, ExecutionTimeout):
            raise DBConnectionError(
                "Could not found service in DB"
            )
        return services_get

    async def create_service(self, service: ServiceModel) -> ServiceDictModel:
        service = jsonable_encoder(service)
        try:
            await self.nosql_conn["services"].insert_one(service)
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not insert service in DB")
        return service

    async def create_product(self, product: ProductModel) -> ProducDictModel:
        product = jsonable_encoder(product)
        try:
            await self.nosql_conn["products"].insert_one(product)
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not insert product in DB")
        return product

    async def update_service(
        self,
        service_id: str,
        service: ServiceUpdateModel
    ):
        query = {"_id": service_id}
        values = {
            "$set": service.dict(exclude_unset=True)
        }
        try:
            await self.nosql_conn["services"].update_one(query, values)
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not update services in DB")

    async def notify(
        self,
        service_product: Union[ServiceModel, ProductModel],
        _type: MessageType
    ):
        message = MessageFormat(
            type=_type.value,
            content=service_product)
        self.messaging_con.produce(
            self.config.kafka_topic,
            message.json(encoder=str).encode("utf-8")
        )
        self.messaging_con.flush()

    async def _get_token(self) -> str:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = f"client_id={self.config.client_id}&client_secret={self.config.client_secret}&grant_type=client_credentials"  # noqa
        try:
            response = requests.post(
                self.config.syscom_token_url,
                headers=headers,
                data=data
            )
            response.raise_for_status()
        except Exception:
            raise TokenError("Problems while getting acces token")
        data = response.json()
        access_token = data.get("access_token")
        if access_token:
            return access_token
        raise TokenError("Problems while getting acces token")
