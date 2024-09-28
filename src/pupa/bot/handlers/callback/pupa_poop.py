from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from pupa.infrastructure.db.repositories import GeneralRepository

router = Router()


@router.callback_query(F.data.startswith("remove_poop_"))
@inject
async def remove_poop(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository]
):
	pupa_id = int(callback.data.split('_')[2])
	await repository.pupa.set_poop_state(pupa_id=pupa_id, status=False)
	await repository.pupa.inscribe_mood(pupa_id=pupa_id, value=10)
	dialog_manager.show_mode = ShowMode.NO_UPDATE
	await callback.message.delete()
