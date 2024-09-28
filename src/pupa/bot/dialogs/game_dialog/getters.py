import time
from sndhdr import tests

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.bot.dialogs import game_dialog
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
	question: [Question, UserQuestions | None] = await repository.questions.get_random_question(
		user_id=user.id,
		question_type=dialog_manager.dialog_data['game_type']
	)
	dialog_manager.dialog_data['answer'] = question[0].answer
	dialog_manager.dialog_data['question_id'] = question[0].id
	dialog_manager.dialog_data['start_time'] = time.time()
	if len(question) > 1:
		dialog_manager.dialog_data['count_user_answers'] = question[1].count_answers
	if dialog_manager.dialog_data['has_media']:
		game_media = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(question[0].media))
	else:
		game_media = ''
	return {
		'questions': question[0].options.split(','),
		'game_text': dialog_manager.dialog_data['game_text'],
		'has_media': dialog_manager.dialog_data['has_media'],
		"game_media": game_media,
		'question_number': dialog_manager.dialog_data['count_answers'] + 1
	}


def getter_question_id(question: str) -> str:
	return question


async def getter_final_menu(
	dialog_manager: DialogManager,
	**_,
):
	final_text, final_media = get_final_data(
		win=dialog_manager.dialog_data['win'],
		count_correct_answers=dialog_manager.dialog_data['true_answers']
	)
	return {
		'final_text': final_text,
		'final_media': final_media
	}


def get_final_data(
	win: bool,
	count_correct_answers: int
):
	if win:
		text = 'Поздравляю! Ты выиграл!, ты молодец!\n Правильных ответов: {count_correct_answers} из 10\n'
		media = MediaAttachment(type=ContentType.DOCUMENT, path="resources/media/gifs/win.gif")
	else:

		text = 'К сожалению, ты проиграл!\n Правильных ответов: {count_correct_answers} из 10\n'
		media = MediaAttachment(type=ContentType.DOCUMENT, path="resources/media/gifs/lose.gif")
	return text, media