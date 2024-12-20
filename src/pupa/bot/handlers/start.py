import asyncio

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from taskiq_redis import RedisScheduleSource

from pupa.bot.states.dialog_states import MainMenuState
from pupa.infrastructure.db.models import Pupa, User
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository
from pupa.infrastructure.scheduler.tasks import decrease_hungry, decrease_mood

router = Router()


@router.message(CommandStart())
@inject
async def start_command(
	message: Message,
	dialog_manager: DialogManager,
	bot: Bot,
	new_user: bool,
	pupa: Pupa,
	user: User,
	redis_source: FromDishka[RedisScheduleSource],
	repository: FromDishka[GeneralRepository]
):
	await message.delete()
	if new_user:
		file = FSInputFile('resources/media/gifs/egg.gif')
		answer_message = await message.answer_document(
			document=file,
			caption='Это яйцо из которого вылупляется Пупа'
		)
		await asyncio.sleep(5)
		await answer_message.delete()
		await dialog_manager.start(
			state=MainMenuState.time_menu,
			mode=StartMode.RESET_STACK,
			show_mode=ShowMode.EDIT
		)
	else:
		await dialog_manager.start(
			state=MainMenuState.main_menu,
			mode=StartMode.RESET_STACK,
			show_mode=ShowMode.DELETE_AND_SEND
		)
