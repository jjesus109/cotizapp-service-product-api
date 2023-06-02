from typing import Any, List

from app.entities.models import (
    ServiceModel,
    ServiceUpdateModel,
    ProductModel,
    ProductResponseSearchModel
)
from app.config import Config
from app.adapters.gateway_i import GatewayInterface
from app.infrastructure.repository_i import RepositoryInterface


class Gateway(GatewayInterface):

    repository: RepositoryInterface
    conf: Config()

    async def get_service(self, service_id: int) -> ServiceModel:
        return await self.repository.get_service_data(service_id)

    async def get_product(self, product_id: int) -> ProductModel:
        return await self.repository.get_product_data(product_id)

    async def search_product(self, word: str) -> List[ProductModel]:
        response = await self.repository.search_products(word)
        return await self._map_response_to_model(response)

    async def search_services_by_name(
        self,
        service_name: str
    ) -> List[ServiceModel]:
        return await self.repository.search_services_by_name(service_name)

    async def search_services_by_description(
        self,
        service_description: str
    ) -> List[Any]:
        return await self.repository.search_services_by_description(
            service_description
        )

    async def create_service(self, service: ServiceModel) -> Any:
        if self.conf.stream_consume:
            response = await self.repository.notify_service(service)
        else:
            response = await self.repository.create_service(service)
        return response

    async def modify_service(self, service: ServiceUpdateModel) -> Any:
        if self.conf.stream_consume:
            response = await self.repository.notify_service_updated(service)
        else:
            response = await self.repository.update_service(service)
        return response

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
