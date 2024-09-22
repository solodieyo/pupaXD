import asyncio

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram_dialog import DialogManager, StartMode

from pupa.bot.states.dialog_states import MainMenuState

router = Router()


@router.message(CommandStart())
async def start_command(message: Message, dialog_manager: DialogManager, bot: Bot):
	await message.delete()
	file = FSInputFile('resources/media/images/test.jpg')
	answer_message = await message.answer_photo(
		photo=file,
		caption='Это яйцо из которого вылупляется пупа'
	)
	await asyncio.sleep(3)
	await answer_message.delete()
	await dialog_manager.start(state=MainMenuState.main_menu, mode=StartMode.RESET_STACK)

