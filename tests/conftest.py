from typing import AsyncGenerator

import pytest
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import CONFIG
from src.domain.products.entities import Product, ProductCategory
from src.domain.users.entities import User
from src.database import DEFAULT_SESSION_FACTORY, engine, Base

from src.presentation.api.v1.auth.dependencies import encode_jwt
from src.presentation.api.v1.auth.schemas import JwtPayloadSchema

from src.main import app


@pytest.fixture(scope="session", autouse=True)
async def prepare_database() -> None:
    assert CONFIG.MODE == "TEST"

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    # Insert initial data
    async with DEFAULT_SESSION_FACTORY() as session:
        async with session.begin():
            # Add users
            admin_user = User(
                email="admin@admin.com",
                name="Admin",
                is_admin=True,
                hashed_password=b''  # Update if you have a specific password hashing method
            )
            base_user = User(
                email="base@base.com",
                name="Base",
                is_admin=False,
                hashed_password=b''  # Update if you have a specific password hashing method
            )
            session.add(admin_user)
            session.add(base_user)

            # Add products
            first_car = Product(
                name="Яблоко",
                category=ProductCategory.FOOD,
                brand="Яблочный сад",
                quantity=29,
                price=75
            )
            second_car = Product(
                name="Груша",
                category=ProductCategory.FOOD,
                brand="Яблочный сад",
                quantity=60,
                price=120
            )
            session.add(first_car)
            session.add(second_car)

        await session.commit()
    yield


@pytest.fixture(scope="session")
async def get_test_session() -> AsyncGenerator[AsyncSession, None]:
    async with DEFAULT_SESSION_FACTORY() as session:
        yield session


@pytest.fixture(scope="function")
async def unauthorized_client() -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as client:
        yield client


@pytest.fixture(scope="function")
async def admin_client(unauthorized_client: AsyncClient) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as client:
        # Set cookie for admin client
        token = encode_jwt(payload=JwtPayloadSchema(id=1, name="Admin"))
        client.cookies.set("token", token)
        yield client


@pytest.fixture(scope="function")
async def authorized_client(unauthorized_client: AsyncClient) -> AsyncClient:
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test/api/v1"
    ) as client:
        # Set cookie for authorized (non-admin) client
        token = encode_jwt(payload=JwtPayloadSchema(id=2, name="Base"))
        client.cookies.set("token", token)
        yield client
