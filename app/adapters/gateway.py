from typing import Any, List
from dataclasses import dataclass

from app.entities.models import (
    ServiceModel,
    ServiceUpdateModel,
    ProductModel,
    ProductResponseSearchModel,
    ServiceDictModel,
    ProducDictModel
)
from app.config import Config
from app.adapters.gateway_i import GatewayInterface
from app.infrastructure.repository_i import RepositoryInterface

from pydantic import BaseSettings
from fastapi.encoders import jsonable_encoder


@dataclass
class Gateway(GatewayInterface):

    repository: RepositoryInterface
    conf: BaseSettings = Config()

    async def get_service(self, service_id: int) -> ServiceDictModel:
        return await self.repository.get_service_data(service_id)

    async def get_product(self, product_id: int) -> ProducDictModel:
        return await self.repository.get_product_data(product_id)

    async def search_product(self, word: str) -> List[ProducDictModel]:
        response = await self.repository.search_products(word)
        return await self._map_response_to_model(response)

    async def search_services_by_name(
        self,
        service_name: str
    ) -> List[ServiceDictModel]:
        return await self.repository.search_services_by_name(service_name)

    async def search_services_by_description(
        self,
        service_description: str
    ) -> List[ServiceDictModel]:
        return await self.repository.search_services_by_description(
            service_description
        )

    async def create_service(self, service: ServiceModel) -> ServiceDictModel:
        if self.conf.stream_consume:
            response = await self.repository.notify(service)
        else:
            response = await self.repository.create_service(service)
        return response

    async def create_product(self, product: Any) -> ProducDictModel:
        if self.conf.stream_consume:
            response = await self.repository.notify(product)
        else:
            response = await self.repository.create_product(product)
        return response

    async def modify_service(
        self,
        service_id: str,
        service: ServiceUpdateModel
    ) -> ServiceDictModel:
        if self.conf.stream_consume:
            service_got = await self.repository.get_service_data(service_id)
            service_model = ServiceModel(**service_got)
            new_service_data = service.dict(exclude_unset=True)
            updated_service = service_model.copy(update=new_service_data)
            await self.repository.notify(
                updated_service
            )
            updated_service = jsonable_encoder(updated_service)
        else:
            await self.repository.update_service(
                service_id,
                service
            )
            updated_service = await self.repository.get_service_data(
                service_id
            )
        return updated_service

    async def _map_response_to_model(
        self,
        raw_data: List[ProductResponseSearchModel]
    ) -> List[ProductModel]:
        return [
            ProductModel(
                title=prs.get("titulo"),
                list_price=prs.get("precios").get("precio_lista"),
                discount_price=prs.get("precios").get("precio_descuento"),
                image=prs.get("img_portada"),
                stock_number=prs.get("existencia").get("nuevo"),
                brand=prs.get("marca"),
                product_id=prs.get("producto_id"),
                model=prs.get("modelo"),
                sat_key=prs.get("sat_key"),
                weight=prs.get("peso"),
            ) for prs in raw_data
        ]
