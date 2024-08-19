from enum import StrEnum

from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base, id_, str256


class ProductCategory(StrEnum):
    FOOD = "FOOD"
    BEVERAGE = "BEVERAGE"
    SNACK = "SNACK"
    DAIRY = "DAIRY"
    OTHER = "OTHER"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[id_]
    name: Mapped[str256] = mapped_column(index=True)
    category: Mapped["ProductCategory"]
    brand: Mapped[str256 | None]
    quantity: Mapped[int]
    price: Mapped[int]
