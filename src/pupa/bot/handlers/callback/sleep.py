from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, ShowMode, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from pupa.bot.states.dialog_states import MainMenuState
from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories import GeneralRepository

router = Router()


@router.callback_query(F.data.startswith("go_sleep_"))
@inject
async def go_sleep(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
	pupa: Pupa,
	repository: FromDishka[GeneralRepository]
):
	await repository.pupa.set_sleep_state(pupa_id=pupa.id, status=True)
	await callback.message.delete()
	await dialog_manager.start(
		state=MainMenuState.sleep,
		show_mode=ShowMode.EDIT,
		mode=StartMode.RESET_STACK
	)