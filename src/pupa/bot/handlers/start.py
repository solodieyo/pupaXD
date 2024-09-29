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

from pupa.bot.enums.question_type import QuestionType
from pupa.bot.states.dialog_states import MainMenuState
from pupa.config import AppConfig
from pupa.infrastructure.db.models import Pupa, User
from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.dto_models.question import QuestionDTO
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
		show_mode=ShowMode.EDIT
	)


@router.message(F.photo)
@inject
async def on_photo(
	message: Message,
	repository: FromDishka[GeneralRepository],
	config: FromDishka[AppConfig]
):
	if message.from_user.id in config.tg.admins_id:
		await repository.questions.add_question(
			file_id=message.photo[-1].file_id,
			true_answer=message.caption,
			question_type=QuestionType.paints
		)
		await message.answer('Вопрос добавлен')
	else:
		await message.delete()