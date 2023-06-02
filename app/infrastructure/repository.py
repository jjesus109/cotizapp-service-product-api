import logging
from typing import List, Any
from dataclasses import dataclass

from app.config import Config
from app.errors import ElementNotFoundError, TokenError
from app.entities.models import ServiceModel, ProductResponseSearchModel
from app.infrastructure.repository_i import RepositoryInterface

import requests
from confluent_kafka import Producer
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import (
    ConnectionFailure,
    ExecutionTimeout
)

config = Config()
log = logging.getLogger(__name__)


@dataclass
class Repository(RepositoryInterface):

    nosql_conn: AsyncIOMotorDatabase
    messaging_con: Producer

    async def get_service_data(self, service_id: int) -> ServiceModel:
        try:
            service = await self.nosql_conn.db["services"].find(
                {
                    "_id": service_id
                }
            )
        except (ConnectionFailure, ExecutionTimeout):
            raise ElementNotFoundError(
                "Service not found in DB"
            )
        return service

    async def get_product_data(self, product_id: int) -> Any:
        try:
            service = await self.nosql_conn.db["products"].find(
                {
                    "_id": product_id
                }
            )
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
        URL = f"{config.syscom_api_url}productos?busqueda={word}"
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
        return raw_data

    async def search_services_by_name(
        self,
        service_name: str
    ) -> List[ServiceModel]:
        try:
            services_get = await self.nosql_conn.db["services"].find(
                {
                    "name": {
                        "$regex": service_name,
                        "$options": "mxsi"
                    }
                }
            ).to_list()
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
            services_get = await self.nosql_conn.db["services"].find(
                {
                    "description": {
                        "$regex": service_description,
                        "$options": "mxsi"
                    }
                }
            ).to_list()
        except (ConnectionFailure, ExecutionTimeout):
            raise ElementNotFoundError(
                "Could not found service in DB"
            )
        return services_get

    async def update_service(self, service: Any) -> Any:
        """Update service in DB

        Args:
            service (Any): service to update

        Returns:
            Any: Service updated
        """

    async def notify_service(self, service: Any):
        """Notification about a service changes in
        messaging system

        Args:
            service (Any): Service to notify

        """

    async def notify_product(self, product: Any):
        """Notification about a product changes in
        messaging system

        Args:
            product (Any): Product to notify

        """

    async def _get_token() -> str:
        headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = f"client_id={config.client_id}&client_secret={config.client_secret}&grant_type=client_credentials"  # noqa
        try:
            response = requests.post(
                config.syscom_token_url,
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
