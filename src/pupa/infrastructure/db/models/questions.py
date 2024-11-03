from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from pupa.bot.enums.question_type import QuestionType
from pupa.infrastructure.db.models import Int16, Base


class Question(Base):
	__tablename__ = 'questions'

	id: Mapped[Int16] = mapped_column(primary_key=True)
	theme_id: Mapped[int] = mapped_column(ForeignKey('themes.id'), nullable=False)
	question: Mapped[Optional[str]]
	options: Mapped[Optional[str]]
	media: Mapped[Optional[str]]
	media_content_type: Mapped[Optional[str]]
	answer: Mapped[str] = mapped_column(nullable=False)