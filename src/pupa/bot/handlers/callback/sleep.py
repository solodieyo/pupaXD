from datetime import datetime, timedelta

from aiogram import Router, F, Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from pytz import timezone
from taskiq_redis import RedisScheduleSource

from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.scheduler.tasks import wake_pupa

router = Router()


@router.callback_query(F.data.startswith("go_sleep_"))
@inject
async def go_sleep(
	callback: CallbackQuery,
	dialog_manager: DialogManager,
	pupa: Pupa,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot],
	redis_source: FromDishka[RedisScheduleSource],
):
	await repository.pupa.set_sleep_state(pupa_id=pupa.id, status=True)
	await callback.message.delete()

	message = await bot.send_document(
		chat_id=callback.from_user.id,
		document=FSInputFile('resources/media/gifs/sleep.gif'),
		caption='Пупа спит...',

	)

	await wake_pupa.schedule_by_time(
		source=redis_source,
		time=datetime.now(tz=timezone('Europe/Moscow')) + timedelta(hours=8),
		pupa_id=pupa.id,
		chat_id=callback.from_user.id,
		message_id=message.message_id
	)