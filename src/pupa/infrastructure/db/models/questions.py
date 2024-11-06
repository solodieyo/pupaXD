from typing import Optional

from aiogram.enums import ContentType
from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from pupa.infrastructure.db.models import Int16, Base


class Question(Base):
	__tablename__ = 'questions'

	id: Mapped[Int16] = mapped_column(primary_key=True)
	theme_id: Mapped[Int16] = mapped_column(ForeignKey('themes.id'), nullable=False)
	question: Mapped[Optional[str]]
	options: Mapped[Optional[str]]
	media: Mapped[Optional[str]]
	media_content_type: Mapped[ContentType] = mapped_column(nullable=True)
	answer: Mapped[str] = mapped_column(nullable=False)