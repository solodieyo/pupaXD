from pathlib import Path
from random import randint

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.bot.utils.checker_pupa_status import check_food_status, check_mood_status, check_iq_status
from pupa.infrastructure.db.models import Pupa, User
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository


@inject
async def get_pupa_status(
	dialog_manager: DialogManager,
	user: User,
	repository: FromDishka[GeneralRepository],
	**_
):
	pupa: Pupa = await repository.pupa.get_or_create_pupa(owner_id=user.id)

	return {
		'hungry': pupa.hungry,
		"mood": pupa.mood,
		"iq": pupa.iq,
		'iq_state': check_iq_status(pupa.iq),
		"hungry_state": check_food_status(pupa.hungry),
		'mood_state': check_mood_status(pupa.mood),

	}


@inject
async def get_main_media(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	user: User,
	**_
):
	pupa: Pupa = await repository.pupa.get_or_create_pupa(owner_id=user.id)

	if dialog_manager.dialog_data.get('no_mood', False):
		media = MediaAttachment(
			type=ContentType.DOCUMENT,
			path=Path(
				f'resources/media/gifs/no_mood_play.gif'
			)
		)
		dialog_manager.dialog_data['no_mood'] = None

	elif 0 <= pupa.iq <= 20:
		media = MediaAttachment(
			type=ContentType.DOCUMENT,
			path=Path(
				f'resources/media/gifs/dumb_pupa.gif'
			)
		)
	else:
		media = MediaAttachment(
			type=ContentType.DOCUMENT,
			path=Path(
				f'resources/media/gifs/main_{randint(1, 3)}.gif'
			)
		)
	return {
		"main_media": media
	}
