import html
from datetime import time

from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq.scheduler.created_schedule import CreatedSchedule
from taskiq.scheduler.scheduled_task import CronSpec
from taskiq_redis import RedisScheduleSource

from pupa.bot.states.dialog_states import SettingsStates
from pupa.bot.utils.parse_user_time import parse_user_time
from pupa.config import AppConfig
from pupa.infrastructure.db.models import Pupa, User
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository
from pupa.infrastructure.scheduler.tasks import sleep_pupa


@inject
async def input_sleep_time(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource]
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']

	parsed_time: time = parse_user_time(time_string=message.text)
	if parsed_time:
		await redis_source.delete_schedule(pupa.sleep_schedule_id)
		sleep_schedule: CreatedSchedule = await sleep_pupa.schedule_by_cron(
			source=redis_source,
			cron=CronSpec(hours=parsed_time.hour, minutes=parsed_time.minute, offset='Europe/Moscow'),
			pupa_id=pupa.id,
			chat_id=message.from_user.id
		)
		await repository.pupa.set_sleep_time(
			pupa_id=pupa.id, time=f"{parsed_time.hour}:{parsed_time.minute}",
			sleep_schedule_id=sleep_schedule.schedule_id
		)
		await message.delete()
		await dialog_manager.start(
			state=SettingsStates.main,
			show_mode=ShowMode.EDIT,
			mode=StartMode.RESET_STACK
		)
	else:
		dialog_manager.dialog_data['wrong_time'] = True


@inject
async def input_issue(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot],
	config: FromDishka[AppConfig],
):
	user: User = dialog_manager.middleware_data['user']
	await message.delete()
	await bot.send_message(
		chat_id=config.tg.idea_channel_id,
		text='<b>Новое предложение!</b>\n\n'
			 f'От пользователя - <a href="t.me/{message.from_user.username}">{html.escape(message.from_user.full_name)}</a>'
			 f' - ID[<code>{message.from_user.id}</code>]\n\n'
			 f'{message.text}',
		disable_web_page_preview=True
	)
	await repository.stats.create_issue(
		user_id=user.id,
		text=message.text
	)
	dialog_manager.show_mode = ShowMode.EDIT
	dialog_manager.dialog_data['sent'] = True
