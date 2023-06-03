import logging
import json
from typing import List, Any
from dataclasses import dataclass

from app.config import Config
from app.errors import ElementNotFoundError, TokenError, InsertionError
from app.entities.models import (
    ServiceModel,
    ServiceUpdateModel,
    ProductResponseSearchModel,
    ProductModel
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


@dataclass
class Repository(RepositoryInterface):

    nosql_conn: AsyncIOMotorDatabase
    messaging_con: Producer
    config: BaseSettings = Config()

    async def get_service_data(self, service_id: int) -> ServiceModel:
        try:
            service = await self.nosql_conn["services"].find(
                {
                    "_id": service_id
                }
            ).to_list(self.config.max_search_elements)
        except (ConnectionFailure, ExecutionTimeout):
            raise ElementNotFoundError(
                "Service not found in DB"
            )
        return service

    async def get_product_data(self, product_id: int) -> Any:
        try:
            service = await self.nosql_conn["products"].find(
                {
                    "_id": product_id
                }
            ).to_list(self.config.max_search_elements)
        except (ConnectionFailure, ExecutionTimeout):
            raise ElementNotFoundError(
                "Service not found in DB"
            )
        return service

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
    ) -> List[ServiceModel]:
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
            raise ElementNotFoundError(
                "Could not found service in DB"
            )
        return services_get

    async def search_services_by_description(
        self,
        service_description: str
    ) -> List[ServiceModel]:
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
            raise ElementNotFoundError(
                "Could not found service in DB"
            )
        return services_get

    async def create_service(self, service: ServiceModel) -> ServiceModel:
        service = jsonable_encoder(service)
        try:
            await self.nosql_conn["services"].insert_one(service)
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not insert service in DB")
        return service

    async def create_product(self, product: ProductModel) -> ProductModel:
        product = jsonable_encoder(product)
        try:
            await self.nosql_conn["products"].insert_one(product)
        except (ConnectionFailure, ExecutionTimeout):
            raise InsertionError("Could not insert product in DB")
        return product

    async def update_service(self, service: Any) -> Any:
        """Update service in DB

        Args:
            service (Any): service to update

        Returns:
            Any: Service updated
        """

    async def notify_service(self, service: ServiceModel) -> ServiceModel:
        json_data = json.dumps(service.json())
        self.messaging_con.produce(
            self.config.kafka_topic,
            json_data.encode("utf-8")
        )
        self.messaging_con.flush()
        return service

    async def notify_product(self, product: ProductModel) -> ProductModel:
        json_data = json.dumps(product.json())
        self.messaging_con.produce(
            self.config.kafka_topic,
            json_data.encode("utf-8")
        )
        self.messaging_con.flush()
        return product

    async def notify_service_updated(self, service: ServiceUpdateModel):
        """Notification about a updating in service changes in
        messaging system

        Args:
            service (Any): Service to notify in changes

        """

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
