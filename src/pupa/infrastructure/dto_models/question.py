from dataclasses import dataclass

from pupa.infrastructure.db.models import UserQuestions
from pupa.infrastructure.db.models.question import Question


@dataclass
class QuestionDTO:
	question: Question | None
	user_question: UserQuestions | None
	options: list[str]
	true_answer: str