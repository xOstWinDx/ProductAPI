from fastapi import APIRouter, Depends, Query
from src.domain.products import ProductService
from src.infrastructure.uow.product import SqlAlchemyProductUnitOfWork
from src.presentation.api.v1.dependencies import authorization_user, authorization_admin
from src.presentation.api.v1.products.schemas import ProductCreateSchema, ProductFilterSchema, ProductGetSchema, \
    ProductUpdateSchema
from src.presentation.api.v1.exceptions import NotFoundExc

router = APIRouter(prefix="/products", tags=["products"])


@router.post("/", status_code=201, description="Create new product")
async def add_product(product_data: ProductCreateSchema, _=Depends(authorization_user)) -> int:
    product_service = ProductService(uow=SqlAlchemyProductUnitOfWork())
    return await product_service.create_product(**product_data.model_dump())


@router.get("/{product_id}", response_model=ProductGetSchema, description="Get product by id")
async def get_product_by_id(product_id: int, _=Depends(authorization_user)):
    product_service = ProductService(uow=SqlAlchemyProductUnitOfWork())
    res = await product_service.get_by_id(product_id)
    if not res:
        raise NotFoundExc("Product not found")
    return res


@router.get("/", response_model=list[ProductGetSchema], description="Get all products")
async def get_all_products(
        filters: ProductFilterSchema = Depends(),
        offset: int = Query(default=0),
        limit: int = Query(default=10, ge=1, le=100),
        _=Depends(authorization_user)
):
    product_service = ProductService(uow=SqlAlchemyProductUnitOfWork())
    res = await product_service.get_all_products(
        offset=offset,
        limit=limit,
        **filters.model_dump(exclude_none=True)
    )
    return res


@router.patch("/{product_id}", description="Update product by id")
async def update_product(
        product_id: int,
        product_data: ProductUpdateSchema,
        _=Depends(authorization_admin)
):
    product_service = ProductService(uow=SqlAlchemyProductUnitOfWork())
    try:
        res = await product_service.update(product_id, **product_data.model_dump(exclude_none=True))
        return res
    except ValueError:
        raise NotFoundExc("Product not found")


@router.delete("/{product_id}", description="Delete product by id", status_code=204)
async def delete_product(product_id: int, _=Depends(authorization_admin)):
    product_service = ProductService(uow=SqlAlchemyProductUnitOfWork())
    try:
        res = await product_service.delete_by_id(product_id)
        return res
    except ValueError:
        raise NotFoundExc("Product not found")
