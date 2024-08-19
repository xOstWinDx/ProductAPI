from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.database import DEFAULT_SESSION_FACTORY
from src.domain.products.interfaces import AbstractProductUnitOfWork
from src.infrastructure.repositories import SqlAlchemyProductRepository


class SqlAlchemyProductUnitOfWork(AbstractProductUnitOfWork):

    def __init__(self, session_factory: async_sessionmaker[AsyncSession] = DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()

    async def __aenter__(self):
        self.session = self.session_factory()
        self.products = SqlAlchemyProductRepository(session=self.session)
        return self
