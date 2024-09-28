from pathlib import Path
from random import randint

from aiogram.enums import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment


async def getter_care_menu(
	dialog_manager: DialogManager,
	**_
):
	food_media = dialog_manager.dialog_data.get('food_media')
	if food_media:
		path = 'resources/media/gifs/food.gif'
	else:
		path = f'resources/media/gifs/main_{randint(1, 3)}.gif'

	return {
		'food_media': food_media,
		'media': MediaAttachment(type=ContentType.DOCUMENT, path=Path(path))
	}