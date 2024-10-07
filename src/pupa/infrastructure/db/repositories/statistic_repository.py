from sqlalchemy import select, func

from pupa.bot.enums.question_type import QuestionType
from pupa.infrastructure.db.models import UserQuestions, Question
from pupa.infrastructure.db.repositories import BaseRepository


class StatisticRepository(BaseRepository):

	async def get_paints_user_stat(self, user_id: int):
		total = await self.session.scalar(
			select(func.count(Question.id))
			.where(Question.id == QuestionType.paints)
		)

		user_total = await self.session.scalar(
			select(func.count(Question.id))
			.where(
				UserQuestions.question_type == QuestionType.paints,
				UserQuestions.user_id == user_id
			)
		)
		return user_total, total
