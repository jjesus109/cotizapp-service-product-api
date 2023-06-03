from typing import Any, List
from abc import ABC, abstractmethod


class RepositoryInterface(ABC):

    @abstractmethod
    async def get_service_data(self, service_id: int) -> Any:
        """_summary_

        Args:
            service_id (int): id to get data about the service

        Returns:
            Any: Service data got
        """

    @abstractmethod
    async def get_product_data(self, product_id: int) -> Any:
        """Get information about a product

        Args:
            product_id (int): product id

        Returns:
            Any: Information about the product
        """

    @abstractmethod
    async def search_products(self, word: str) -> List[Any]:
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
        """Create service in DB

        Args:
            service (Any): service to update

        Returns:
            Any: Service updated
        """

    @abstractmethod
    async def create_product(self, product: Any) -> Any:
        """Create a product in DB

        Args:
            product (Any): product to insert

        Returns:
            Any: product created
        """

    @abstractmethod
    async def update_service(self, service_id: str, service: Any) -> Any:
        """Update service in DB

        Args:
            service_id (str): service id to update data
            service (Any): service to update

        Returns:
            Any: Service updated
        """

    @abstractmethod
    async def notify_service(self, service: Any):
        """Notification about a service changes in
        messaging system

        Args:
            service (Any): Service to notify

        """

    @abstractmethod
    async def notify_service_updated(self, service_id: str, service: Any):
        """Notification about a updating in service changes in
        messaging system

        Args:
            service_id (str): service id to update data
            service (Any): Service to notify in changes

        """

    @abstractmethod
    async def notify_product(self, product: Any):
        """Notification about a product changes in
        messaging system

        Args:
            product (Any): Product to notify

        """
