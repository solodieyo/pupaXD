import time

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.infrastructure.db.models import User
from pupa.infrastructure.db.models.theme import Theme
from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.dto_models.question import QuestionDTO, ThemeDTO


@inject
async def journey_game_getter(
	dialog_manager: DialogManager,
	user: User,
	repository: FromDishka[GeneralRepository],
	**_
):
	question: QuestionDTO = await repository.questions.get_random_question(
		user_id=user.id,
		theme_id=dialog_manager.dialog_data['theme_id']
	)

	dialog_manager.dialog_data.update(
		skip=question.skip,
		answer=question.question.answer,
		question_id=question.question.id,
		start_time=time.time()
	)

	if question.user_question:
		dialog_manager.dialog_data['count_user_answers'] = question.user_question.count_answers
	if dialog_manager.dialog_data['has_media']:
		game_media = MediaAttachment(type=ContentType.PHOTO, file_id=MediaId(question.question.media))
	else:
		game_media = ''
	return {
		'questions': question.options,
		'game_text': dialog_manager.dialog_data['game_text'],
		'has_media': dialog_manager.dialog_data['has_media'],
		"game_media": game_media,
		'question_number': dialog_manager.dialog_data['count_answers'] + 1
	}


def getter_theme_select(theme: ThemeDTO) -> int:
	return theme.theme_id


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
		text = f'Поздравляю! Ты выиграл!, ты молодец!\n Правильных ответов: {count_correct_answers} из 10\n'
		media = MediaAttachment(type=ContentType.DOCUMENT, path="resources/media/gifs/win.gif")
	else:
		text = f'К сожалению, Ты проиграл!\n Правильных ответов: {count_correct_answers} из 10\n'
		media = MediaAttachment(type=ContentType.DOCUMENT, path="resources/media/gifs/lose.gif")
	return text, media


@inject
async def getter_themes(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	user: User,
	**_
):
	themes = await repository.theme.get_themes()
	return {
		'themes': await _themes_to_dto(themes, user, repository),
	}


async def _themes_to_dto(
	themes: list[Theme | None],
	user: User,
	repository: GeneralRepository
) -> list[ThemeDTO]:
	new_themes = []
	for theme in themes:
		if theme:
			user_count, total_count = await repository.stats.get_stats_per_theme(
				user_id=user.id, theme_id=theme.id
			)
			if user_count != total_count:
				user_progres = f'{user_count}/{total_count}'
			else:
				user_progres = f'{user_count}/{total_count} 🏆'
			new_themes.append(
				ThemeDTO(
					theme_id=theme.id,
					theme_name=theme.theme_name,
					user_progres=user_progres
				)
			)
	return new_themes
