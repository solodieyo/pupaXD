from datetime import datetime, timedelta

from sqlalchemy import select, func, and_, update

from pupa.bot.enums.question_type import QuestionType
from pupa.infrastructure.db.models.question import Question
from pupa.infrastructure.db.models.user_questions import UserQuestions
from pupa.infrastructure.db.repositories import BaseRepository

INTERVALS = {
	1: 1,
	2: 3,
	3: 7,
	4: 14,
	5: 30,
	6: 90,
	7: 180,
	8: 365,
	9: 750
}


class QuestionRepository(BaseRepository):

	async def add_question(self):
		pass

	async def get_random_question(self, user_id: int, question_type: QuestionType):
		now_date = datetime.now().date()
		question = await self.session.execute(
			select(Question, UserQuestions)
			.join(
				UserQuestions,
				and_(
					UserQuestions.question_id == Question.id,
					UserQuestions.user_id == user_id,
				),
				isouter=True
			)
			.where(
				and_(
					now_date >= func.date(UserQuestions.interval_date),
					Question.question_type == question_type
				)
			)
			.order_by(func.random())
			.limit(1)
		)
		return question.scalars().all()[0]

	async def user_correct_answer_question(self, question_id: int, user_id: int, count_answers: int):
		if count_answers == 0:
			user_question = UserQuestions(
				question_id=question_id,
				user_id=user_id,
				count_answers=count_answers,
				interval_date=datetime.now() + timedelta(days=1)
			)
			self.session.add(user_question)
		else:
			await self.session.execute(
				update(UserQuestions)
				.where(
					and_(
						UserQuestions.question_id == Question.id,
						UserQuestions.user_id == user_id,
					)
				).values(
					count_answers=count_answers,
					interval_date=datetime.now() + timedelta(days=INTERVALS[count_answers])
				)
			)
		await self.session.commit()

