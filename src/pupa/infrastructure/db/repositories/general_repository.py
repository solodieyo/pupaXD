from sqlalchemy.ext.asyncio import AsyncSession

from pupa.infrastructure.db.repositories import BaseRepository
from pupa.infrastructure.db.repositories.pupa_repository import PupaRepository
from pupa.infrastructure.db.repositories.question_repository import QuestionRepository
from pupa.infrastructure.db.repositories.statistic_repository import StatisticRepository
from pupa.infrastructure.db.repositories.user_repository import UserRepository


class GeneralRepository(BaseRepository):
	def __init__(self, session: AsyncSession) -> None:
		super().__init__(session=session)
		self.user = UserRepository(session=session)
		self.pupa = PupaRepository(session=session)
		self.questions = QuestionRepository(session=session)
		self.stats = StatisticRepository(session=session)
