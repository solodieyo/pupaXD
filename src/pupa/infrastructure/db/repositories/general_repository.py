from sqlalchemy.ext.asyncio import AsyncSession

from pupa.infrastructure.db.repositories import BaseRepository
from pupa.infrastructure.db.repositories.user_repository import UserRepository


class GeneralRepository(BaseRepository):
	def __init__(self, session: AsyncSession) -> None:
		super().__init__(session=session)
		self.user = UserRepository(session=session)
