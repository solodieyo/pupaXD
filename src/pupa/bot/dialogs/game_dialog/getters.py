import time

from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.infrastructure.db.models import User, Question
from pupa.infrastructure.db.models.user_questions import UserQuestions
from pupa.infrastructure.db.repositories import GeneralRepository


@inject
async def journey_game_getter(
	dialog_manager: DialogManager,
	user: User,
	repository: FromDishka[GeneralRepository],
	**_
):
	question: (Question, UserQuestions | None) = await repository.questions.get_random_question(
		user_id=user.id,
		question_type=dialog_manager.dialog_data['game_type']
	)
	dialog_manager.dialog_data['answer'] = question[0].answer
	dialog_manager.dialog_data['question_id'] = question.id
	dialog_manager.dialog_data['start_time'] = time.time()
	if question[1]:
		dialog_manager.dialog_data['count_user_answers'] = question[1].count_answers

	return {
		'questions': question.options.split(',') if question else None,
		'game_text': dialog_manager.dialog_data['game_text'],
		'has_media': dialog_manager.dialog_data['has_media'],

	}


def getter_question_id(question: str) -> str:
	return question