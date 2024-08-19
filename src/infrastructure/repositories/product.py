from typing import Sequence

from sqlalchemy import insert, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.products.entities import Product
from src.domain.products import AbstractProductRepository


class SqlAlchemyProductRepository(AbstractProductRepository):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_by_data(self, **product_data) -> int:
        stmt = (
            insert(Product).
            values(**product_data).
            returning(Product.id)
        )
        res = await self.session.execute(stmt)
        return res.scalar()

    async def get_by_id(self, product_id: int) -> Product | None:
        return await self.session.get(Product, product_id)

    async def get_all(self, offset: int, limit: int, **filter_by) -> Sequence[Product]:
        query = (
            select(Product).
            offset(offset).
            limit(limit)
        )
        filters = []

        for key, value in filter_by.items():
            if key == "max_quantity":
                filters.append(Product.quantity <= value)
            elif key == "min_quantity":
                filters.append(Product.quantity >= value)
            elif key == "max_price":
                filters.append(Product.price <= value)
            elif key == "min_price":
                filters.append(Product.price >= value)
            else:
                filters.append(getattr(Product, key) == value)

        if filters:
            query = query.where(*filters)
        res = await self.session.scalars(query)
        return res.all()

    async def update_by_id(self, product_id: int, **new_data) -> int:
        stmt = (
            update(Product).
            where(Product.id == product_id).
            values(**new_data)
        )
        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore

    async def delete_by_id(self, product_id: int) -> int:
        stmt = (
            delete(Product).
            where(Product.id == product_id)
        )
        result = await self.session.execute(stmt)
        return result.rowcount  # type: ignore