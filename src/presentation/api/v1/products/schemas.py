from fastapi import Query, HTTPException
from pydantic import BaseModel, Field

from src.domain.products.entities import ProductCategory
from src.schemas import BaseSchema


class ProductCreateSchema(BaseModel):
    name: str = Field(max_length=255, min_length=1)
    category: ProductCategory
    brand: str | None = Field(None, max_length=255)
    quantity: int = Field(ge=0)
    price: int = Field(gt=0)


class ProductUpdateSchema(BaseModel):
    name: str | None = Field(default=None, max_length=255, min_length=1)
    category: ProductCategory | None = None
    brand: str | None = Field(default=None, max_length=255)
    quantity: int | None = Field(default=None, ge=0)
    price: int | None = Field(default=None, gt=0)


class ProductGetSchema(ProductCreateSchema, BaseSchema):
    ...


class ProductFilterSchema:
    def __init__(
            self,
            name: str | None = Query(default=None, max_length=255, min_length=1),
            category: ProductCategory | None = Query(default=None),
            brand: str | None = Query(default=None, max_length=255),
            min_price: int | None = Query(default=None, ge=0),
            max_price: int | None = Query(default=None),
            min_quantity: int | None = Query(default=None, ge=0),
            max_quantity: int | None = Query(default=None)
    ):
        self.name = name
        self.category = category
        self.brand = brand
        self.min_price = min_price
        self.max_price = max_price
        self.min_quantity = min_quantity
        self.max_quantity = max_quantity

        self.validate()

    def validate(self):
        if self.min_price is not None and self.max_price is not None and self.min_price > self.max_price:
            raise HTTPException(status_code=400, detail='min_price must be less than or equal to max_price')
        if self.min_quantity is not None and self.max_quantity is not None and self.min_quantity > self.max_quantity:
            raise HTTPException(status_code=400, detail='min_quantity must be less than or equal to max_quantity')

    def model_dump(self, exclude_none: bool = False) -> dict:
        data = {
            'name': self.name,
            'category': self.category,
            'brand': self.brand,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'min_quantity': self.min_quantity,
            'max_quantity': self.max_quantity,
        }
        if exclude_none:
            return {k: v for k, v in data.items() if v is not None}
        return data
