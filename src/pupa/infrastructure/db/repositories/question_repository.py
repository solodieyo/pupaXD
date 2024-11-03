from datetime import datetime, timedelta

from aiogram.enums import ContentType
from sqlalchemy import select, func, and_, update, delete

from pupa.bot.dialogs.admin.dialog import theme_select, questions
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
		question: str,
		media: str,
		answer: str,
		theme_id: int,
		media_content_type: ContentType,
		options: str = None,
	):
		question = Question(
			theme_id=theme_id,
			media=media,
			answer=answer,
			media_content_type=media_content_type,
			options=options,
		)
		self.session.add(question)
		await self.session.commit()

	async def get_random_question(self, user_id: int, theme_id: int):
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
					Question.theme_id == theme_id
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
					Question.theme_id == theme_id
				).limit(1)
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
				skip=True
			)

	async def user_correct_answer_question(
		self,
		question_id: int,
		user_id: int,
		count_answers: int,
		theme_id: int,
	):
		if count_answers == 0:
			user_question = UserQuestions(
				question_id=question_id,
				user_id=user_id,
				count_answers=count_answers,
				interval_date=datetime.now() + timedelta(days=1),
				theme_id=theme_id
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

	async def get_questions_by_theme(self, theme_id: int):
		questions = await self.session.execute(
			select(Question)
			.where(Question.theme_id == theme_id)
		)
		return questions.scalars().all()

	async def get_question(self, question_id: int):
		question = await self.session.scalar(
			select(Question).where(Question.id == question_id)
		)
		return question

	async def delete_question(self, question_id: int):
		await self.session.execute(
			delete(Question).where(Question.id == question_id)
		)
		await self.session.commit()

	async def update_question_answer(self, question_id: int, answer: str):
		await self.session.execute(
			update(Question).where(Question.id == question_id).values(answer=answer)
		)
		await self.session.commit()

	async def update_question_text(self, question_id: int, question: str):
		await self.session.execute(
			update(Question).where(Question.id == question_id).values(question=question)
		)
		await self.session.commit()

	async def update_question_media_and_text(
		self, question_id: int,
		media: str,
		content_type: str,
		question: str
	):
		await self.session.execute(
			update(Question).where(Question.id == question_id).values(
				media=media,
				media_content_type=content_type,
				question=question
			)
		)
		await self.session.commit()

	async def update_question_media(self, question_id: int, media: str, content_type: str):
		await self.session.execute(
			update(Question).where(Question.id == question_id).values(
				media=media,
				media_content_type=content_type
			)
		)
		await self.session.commit()