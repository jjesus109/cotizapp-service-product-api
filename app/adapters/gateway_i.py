from typing import Any, List
from abc import ABC, abstractmethod


class GatewayInterface(ABC):

    @abstractmethod
    async def get_service(self, service_id: int) -> Any:
        """Get service data

        Args:
            service_id (int): id to get data about the service

        Returns:
            Any: Service data got+ get_service(service_id: Int): <T>
        """

    @abstractmethod
    async def get_product(self, product_id: int) -> Any:
        """Get information about a product

        Args:
            product_id (int): product id

        Returns:
            Any: Information about the product
        """

    @abstractmethod
    async def search_product(self, word: str) -> List[Any]:
        """Word to search into product catalog

        Args:
            word (str): word to search

        Returns:
            List[Any]: list of match product
        """

    @abstractmethod
    async def search_services_by_name(self, service_name: str) -> List[Any]:
        """Search service by name

        Args:
            service_name (str): Service name to search

        Returns:
            List[Any]: List of services matches
        """

    @abstractmethod
    async def search_services_by_description(
        self,
        service_description: str
    ) -> List[Any]:
        """Search service by description

        Args:
            service_name (str): Service description to search

        Returns:
            List[Any]: List of services matches
        """

    @abstractmethod
    async def create_service(self, service: Any) -> Any:
        """Create a new service in DB

        Args:
            service (Any): service to create
            strategy (Strategy): strategy to execute in updating

        Returns:
            Any: service created
        """

    @abstractmethod
    async def modify_service(self, service: Any) -> Any:
        """Update an existing service

        Args:
            service (Any): service to update
            strategy (Strategy): strategy to execute in updating

        Returns:
            Any: Service modified
        """
