from datetime import date, timedelta

from sqlalchemy import select, func

from pupa.infrastructure.db.models import UserQuestions, User, Question
from pupa.infrastructure.db.models.issue import Issue
from pupa.infrastructure.db.repositories.base import BaseRepository


class StatisticRepository(BaseRepository):
	async def create_issue(self, text: str, user_id: int):
		issue = Issue(
			issue_text=text,
			from_user_id=user_id
		)

		self.session.add(issue)
		await self.session.commit()

	async def get_user_count(self):
		return await self.session.scalar(select(func.count(User.id)))

	async def get_user_count_day(self):
		return await self.session.scalar(
			select(func.count(User.id))
			.where(func.date(User.created_at) == date.today())
		)

	async def get_user_count_month(self):
		return await self.session.scalar(
			select(func.count(User.id))
			.where(func.date(User.created_at).between(date.today() - timedelta(days=30), date.today()))
		)

	async def get_user_count_week(self):
		return await self.session.scalar(
			select(func.count(User.id))
			.where(func.date(User.created_at).between(date.today() - timedelta(days=7), date.today()))
		)

	async def get_stats_per_theme(self, user_id: int, theme_id: int):
		user_count = await self.session.scalar(
			select(func.count(func.distinct(UserQuestions.question_id)))
			.where(
				UserQuestions.user_id == user_id,
				UserQuestions.theme_id == theme_id
			)
		)
		total_count = await self.session.scalar(
			select(func.count(Question.id))
			.where(Question.theme_id == theme_id)
		)
		return user_count, total_count