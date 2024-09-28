import asyncio
from datetime import timedelta, datetime
from importlib.util import source_hash

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from taskiq_redis import RedisScheduleSource

from pupa.bot.states.dialog_states import MainMenuState
from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.scheduler.tasks import decrease_hungry, decrease_mood, test_task

router = Router()


@router.message(CommandStart())
@inject
async def start_command(
	message: Message,
	dialog_manager: DialogManager,
	bot: Bot,
	new_user: bool,
	pupa: Pupa,
	redis_source: FromDishka[RedisScheduleSource]
):
	if new_user:
		file = FSInputFile('resources/media/gifs/egg.gif')
		answer_message = await message.answer_document(
			document=file,
			caption='Это яйцо из которого вылупляется пупа'
		)
		await asyncio.sleep(5)
		await answer_message.delete()
		await decrease_hungry.schedule_by_cron(
			source=redis_source,
			cron='*/5 * * * *',
			pupa_id=pupa.id
		)
		await decrease_mood.schedule_by_cron(
			source=redis_source,
			cron='*/5 * * * *',
			pupa_id=pupa.id
		)
	await dialog_manager.start(
		state=MainMenuState.main_menu,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.DELETE_AND_SEND
	)


# @router.message(F.photo)
# @inject
# async def on_photo(
# 	message: Message,
# 	repository: FromDishka[GeneralRepository]
# ):
# 	question = message.caption.split('|')
# 	await repository.questions.add_question(
# 		file_id=message.photo[-1].file_id,
# 		true_answer=question[1],
# 		options=question[0],
# 		question_type=QuestionType.paints
# 	)
