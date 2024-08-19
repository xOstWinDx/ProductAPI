import logging

from src.domain.products.entities import Product, ProductCategory
from src.domain.products.interfaces import AbstractProductUnitOfWork

logger = logging.getLogger("domain.products.service")


class ProductService:

    def __init__(self, uow: AbstractProductUnitOfWork):
        self.uow = uow

    async def create_product(
            self,
            name: str,
            category: ProductCategory,
            brand: str | None,
            quantity: int,
            price: int
    ) -> int:
        logger.debug(
            "Create product: "
            "name=%s, "
            "category=%s, "
            "brand=%s, "
            "quantity=%s, "
            "price=%s",
            name, category, brand, quantity, price
        )
        try:
            async with self.uow as uow:
                res = await uow.products.create_by_data(
                    name=name,
                    category=category,
                    brand=brand,
                    quantity=quantity,
                    price=price
                )
                await uow.commit()
                return res
        except Exception as e:
            logger.exception("Exception while creating product: %s", e)
            raise

    async def get_all_products(
            self,
            offset: int,
            limit: int,
            **filter_by
    ) -> list[Product]:
        logger.debug("Get all products: %s", filter_by)
        try:
            async with self.uow as uow:
                res = await uow.products.get_all(
                    offset=offset,
                    limit=limit,
                    **filter_by
                )
                await uow.commit()
                return res
        except Exception as e:
            logger.exception("Exception while getting all products: %s", e)
            raise

    async def get_by_id(self, product_id: int) -> Product:
        logger.debug("Get product by id: %s", product_id)
        try:
            async with self.uow as uow:
                res = await uow.products.get_by_id(product_id=product_id)
                return res
        except Exception as e:
            logger.exception("Exception while getting product by id: %s", e)
            raise

    async def update(self, product_id: int, **new_data) -> None:
        logger.debug("Update product: %s", product_id)
        try:
            async with self.uow as uow:
                row_count = await uow.products.update_by_id(product_id=product_id, **new_data)
                await uow.commit()
                if row_count == 0:
                    raise ValueError("Product not found")
        except Exception as e:
            logger.exception("Exception while updating product: %s", e)
            raise

    async def delete_by_id(self, product_id: int) -> None:
        logger.debug("Delete product: %s", product_id)
        try:
            async with self.uow as uow:
                row_count = await uow.products.delete_by_id(product_id=product_id)
                await uow.commit()
                if row_count == 0:
                    raise ValueError("Product not found")
        except Exception as e:
            logger.exception("Exception while deleting product: %s", e)
            raise
