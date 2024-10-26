from asyncio import sleep
from datetime import timedelta, datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode


router = Router()


@router.callback_query(F.data == 'eat_pupa')
async def eat_pupa(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
):
	dialog_manager.show_mode = ShowMode.NO_UPDATE
	await callback.message.delete()


@router.callback_query(F.data == 'delete_message')
async def delete_message_pupa(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
):
	dialog_manager.show_mode = ShowMode.NO_UPDATE
	await callback.message.delete()
