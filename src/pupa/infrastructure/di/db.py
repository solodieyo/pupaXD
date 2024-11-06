from typing import AsyncIterable

from dishka import Provider, Scope, from_context, provide
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, AsyncSession

from pupa.config import AppConfig
from pupa.infrastructure.db.base import create_engine, create_pool
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository


class DbProvider(Provider):
	scope = Scope.APP

	config = from_context(AppConfig)

	@provide
	async def get_engine(self, config: AppConfig) -> AsyncIterable[AsyncEngine]:
		engine = create_engine(config)
		yield engine
		await engine.dispose(True)

	@provide
	def get_pool(self, engine: AsyncEngine) -> async_sessionmaker:
		return create_pool(engine)

	@provide(scope=Scope.REQUEST)
	async def get_session(self, pool: async_sessionmaker) -> AsyncIterable[AsyncSession]:
		async with pool() as session_pool:
			yield session_pool

	@provide(scope=Scope.REQUEST)
	async def get_db(self, session: AsyncSession) -> GeneralRepository:
		return GeneralRepository(session=session)