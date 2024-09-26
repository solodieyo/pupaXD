from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.bot.utils.checker_pupa_statuses import check_food_status, check_mood_status
from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories import GeneralRepository


@inject
async def get_pupa_status(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	pupa: Pupa,
	**_
):
	return {
		'hungry': pupa.hungry,
		"mood": pupa.mood,
		"hungry_state": check_food_status(pupa.hungry),
		'mood_state': check_mood_status(pupa.mood)
	}