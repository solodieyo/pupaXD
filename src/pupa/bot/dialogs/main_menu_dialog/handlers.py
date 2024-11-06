from datetime import time

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq.scheduler.created_schedule import CreatedSchedule
from taskiq.scheduler.scheduled_task import CronSpec
from taskiq_redis import RedisScheduleSource

from pupa.bot.states.dialog_states import MainMenuState, GameStates
from pupa.bot.utils.parse_user_time import parse_user_time
from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository
from pupa.infrastructure.scheduler.tasks import sleep_pupa


async def on_how_pupa(
	_,
	__,
	dialog_manager: DialogManager
):
	await dialog_manager.show(
		show_mode=ShowMode.EDIT
	)


async def on_game_start(
	callback: CallbackQuery,
	__,
	dialog_manager: DialogManager,
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']

	if pupa.mood < 30:
		dialog_manager.dialog_data['no_mood'] = True
		await callback.answer('Пупа не в настроении играть.')
	else:
		await dialog_manager.start(
			GameStates.pupa_journey_select_theme,
			show_mode=ShowMode.EDIT
		)


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
			state=MainMenuState.main_menu,
			show_mode=ShowMode.EDIT,
			mode=StartMode.RESET_STACK
		)
	else:
		dialog_manager.dialog_data['wrong_time'] = True


@inject
async def on_wake_up(
	_,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']

	await repository.pupa.set_sleep_state(pupa_id=pupa.id, status=False)
	await dialog_manager.start(
		state=MainMenuState.main_menu,
		show_mode=ShowMode.EDIT,
		mode=StartMode.RESET_STACK
	)