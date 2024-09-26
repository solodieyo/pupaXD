from typing import Optional

from sqlalchemy.orm import mapped_column, Mapped

from pupa.bot.enums.question_type import QuestionType
from pupa.infrastructure.db.models import Int16, Base


class Question(Base):
	__tablename__ = 'questions'
	id: Mapped[Int16] = mapped_column(primary_key=True)
	question = mapped_column(nullable=True)
	options: Mapped[Optional[str]]
	question_type: Mapped[QuestionType]
	media: Mapped[Optional[str]]
	answer = mapped_column(nullable=False)