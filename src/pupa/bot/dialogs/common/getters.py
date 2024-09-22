from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.infrastructure.db.repositories import GeneralRepository


@inject
async def get_pupa_status(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_
):
	pass