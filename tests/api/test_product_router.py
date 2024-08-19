import pytest
from httpx import AsyncClient
from src.domain.products.entities import ProductCategory


@pytest.mark.parametrize(
    "name, category, brand, quantity, price, status_code",
    [
        ("Product1", ProductCategory.FOOD, "Brand1", 100, 10000, 201),
        ("Product2", ProductCategory.BEVERAGE, "Brand2", 200, 30000, 201),
        ("Product3", ProductCategory.SNACK, "Brand3", "Incorrect", 345000, 422),
        ("Product4", "Incorrect", "Brand4", 500, 450000, 422),
        ("Product5", ProductCategory.FOOD, "Brand5", 430, 5000000, 201)
    ]
)
async def test_create_product(
        authorized_client: AsyncClient,
        name: str,
        category: ProductCategory,
        brand: str,
        quantity: int,
        price: int,
        status_code: int
):
    response = await authorized_client.post(
        "/products/",
        json={
            "name": name,
            "category": category,
            "brand": brand,
            "quantity": quantity,
            "price": price
        }
    )
    assert response.status_code == status_code


async def test_get_all_products(authorized_client: AsyncClient):
    response = await authorized_client.get("/products/")
    assert response.status_code == 200
    assert len(response.json()) >= 4


async def test_update_product(authorized_client: AsyncClient, admin_client: AsyncClient):
    new_data = {
        "name": "UpdatedProduct",
        "category": ProductCategory.DAIRY,
        "brand": "Обновлённый продукт",
        "quantity": 5,
        "price": 100
    }
    auth_response = await authorized_client.patch(
        "/products/1",
        json=new_data
    )
    admin_response = await admin_client.patch(
        "/products/1",
        json=new_data
    )
    assert auth_response.status_code == 403
    assert admin_response.status_code == 200


async def test_delete_product(authorized_client: AsyncClient, admin_client: AsyncClient):
    auth_response = await authorized_client.delete("/products/2")
    admin_response = await admin_client.delete("/products/2")
    assert auth_response.status_code == 403
    assert admin_response.status_code == 200

    get_response = await authorized_client.get("/products/2")
    assert get_response.status_code == 404
