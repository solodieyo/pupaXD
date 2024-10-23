from datetime import datetime, timedelta

from sqlalchemy import select, func, and_, update

from pupa.bot.enums.question_type import QuestionType
from pupa.infrastructure.db.models import Question
from pupa.infrastructure.db.models.user_questions import UserQuestions
from pupa.infrastructure.db.repositories import BaseRepository
from pupa.infrastructure.dto_models.question import QuestionDTO

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

	async def add_question(
		self,
		file_id: str,
		true_answer: str,
		question_type: QuestionType,
		options: str = None,
	):
		question = Question(
			media=file_id,
			answer=true_answer,
			options=options,
			question_type=question_type
		)
		self.session.add(question)
		await self.session.commit()

	async def get_random_question(self, user_id: int, question_type: QuestionType):
		now_date = datetime.now().date()
		question = await self.session.execute(
			select(Question, UserQuestions)
			.outerjoin(
				UserQuestions,
				and_(
					UserQuestions.question_id == Question.id,
					UserQuestions.user_id == user_id,
				),
			)
			.where(
				and_(
					(UserQuestions.id == None) |  # Если UserQuestions не существует
					(now_date >= func.date(UserQuestions.interval_date)),
					Question.question_type == question_type
				)
			)
			.order_by(func.random())
			.limit(1)
		)

		res = question.scalars().all()
		if res:
			options = await self.session.execute(
				select(func.distinct(Question.answer))
				.where(Question.answer != res[0].answer)
				.limit(3)
			)
			return QuestionDTO(
				*res,
				options=options.scalars().all(),
			)
		else:
			question = await self.session.execute(
				select(Question, UserQuestions)
				.outerjoin(
					UserQuestions,
					and_(
						UserQuestions.question_id == Question.id,
						UserQuestions.user_id == user_id,
					),
				).order_by(func.random())
				.where(
					Question.question_type == question_type
				)
			)
			res = question.scalars().all()
			options = await self.session.execute(
				select(func.distinct(Question.answer))
				.where(Question.answer != res[0].answer)
				.limit(3)
			)
			return QuestionDTO(
				*res,
				options=options.scalars().all(),
			)

	async def user_correct_answer_question(
		self,
		question_id: int,
		user_id: int,
		count_answers: int,
		question_type: QuestionType = None,
	):
		if count_answers == 0:
			user_question = UserQuestions(
				question_id=question_id,
				user_id=user_id,
				count_answers=count_answers,
				interval_date=datetime.now() + timedelta(days=1),
				question_type=question_type
			)
			self.session.add(user_question)
		else:
			question = await self.session.scalar(select(
				UserQuestions
			).where(
				and_(
					UserQuestions.question_id == question_id,
					UserQuestions.user_id == user_id,
				)))
			if question.interval_date < datetime.now().date():
				return
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
