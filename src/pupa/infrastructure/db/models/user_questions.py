from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from pupa.bot.enums.question_type import QuestionType
from pupa.infrastructure.db.models import Int16, Base, Int64


class UserQuestions(Base):
	__tablename__ = 'user_questions'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	question_id: Mapped[Int16] = mapped_column(
		ForeignKey('questions.id', ondelete="CASCADE"),
		nullable=False
	)
	user_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'), nullable=False)
	theme_id: Mapped[Int16] = mapped_column(ForeignKey('themes.id'), nullable=False)
	count_answers: Mapped[Int16] = mapped_column(nullable=False, default=0)
	interval_date: Mapped[datetime] = mapped_column(nullable=True)