from pathlib import Path
from random import randint

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from pupa.bot.utils.checker_pupa_status import check_food_status, check_mood_status
from pupa.infrastructure.db.models import Pupa


async def get_pupa_status(
	dialog_manager: DialogManager,
	pupa: Pupa,
	**_
):
	return {
		'hungry': pupa.hungry,
		"mood": pupa.mood,
		"hungry_state": check_food_status(pupa.hungry),
		'mood_state': check_mood_status(pupa.mood),
	}


async def get_main_media(
	dialog_manager: DialogManager,
	**_
):
	media = MediaAttachment(
		type=ContentType.DOCUMENT,
		path=Path(
			f'resources/media/gifs/main_{randint(1, 3)}.gif'
		)
	)
	return {
		"main_media": media
	}
