from dataclasses import dataclass
from random import shuffle
from typing import Sequence, Union, Optional

from sqlalchemy import Row

from pupa.infrastructure.db.models import UserQuestions
from pupa.infrastructure.db.models import Question


@dataclass
class QuestionDTO:
	question: Optional[Question] = None
	user_question: Optional[UserQuestions] = None
	options: Optional[Sequence[Row[tuple[str]]]] = None
	skip: Optional[bool] = False

	def __post_init__(self):
		if self.options:
			self.options = list(self.options) + [self.question.answer]
			shuffle(self.options)


@dataclass
class ThemeDTO:
	theme_id: Optional[int] = None
	theme_name: Optional[str] = None
	user_progres: Optional[str] = None
