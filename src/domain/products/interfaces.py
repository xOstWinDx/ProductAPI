from abc import ABC, abstractmethod
from typing import Sequence

from src.domain.products.entities import Product


class AbstractProductUnitOfWork(ABC):

    @abstractmethod
    async def commit(self):
        raise NotImplementedError

    @abstractmethod
    async def rollback(self):
        raise NotImplementedError

    @abstractmethod
    async def __aenter__(self):
        self.products = AbstractProductRepository()
        return self

    async def __aexit__(self, exn_type, exn_value, traceback):
        await self.rollback()


class AbstractProductRepository(ABC):
    @abstractmethod
    async def create_by_data(self, **product_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_by_id(self, product_id: int) -> Product:
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[Product]:
        raise NotImplementedError

    @abstractmethod
    async def update_by_id(self, product_id: int, **new_data) -> int:
        raise NotImplementedError

    @abstractmethod
    async def delete_by_id(self, product_id: int) -> int:
        raise NotImplementedError
