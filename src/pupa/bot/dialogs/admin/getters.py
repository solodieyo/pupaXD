from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.infrastructure.db.models import Question
from pupa.infrastructure.db.models.theme import Theme
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository


@inject
async def getter_themes(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_,
):
	themes = await repository.theme.get_themes()

	return {
		'themes': themes
	}


def themes_item_id_getter(theme: Theme) -> int:
	return theme.id


@inject
async def getter_questions(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_,
):
	questions = await repository.questions.get_questions_by_theme(
		theme_id=dialog_manager.dialog_data['theme_id']
	)

	return {
		'questions': questions
	}


def questions_item_id_getter(question: Question) -> int:
	return question.id


@inject
async def getter_question(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_,
):
	question = await repository.questions.get_question(
		question_id=dialog_manager.dialog_data['question_id']
	)

	if question.media:
		media = MediaAttachment(
			file_id=MediaId(question.media),
			type=question.media_content_type
		)
	else:
		media = None

	return {
		'question': question.question,
		'answer': question.answer,
		'media': media
	}