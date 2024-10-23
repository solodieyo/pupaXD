
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager


router = Router()


@router.callback_query(F.data == 'eat_pupa')
async def eat_pupa(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
):
	await callback.message.delete()