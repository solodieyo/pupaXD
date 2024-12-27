from asyncio import sleep
from datetime import datetime, timedelta

from aiogram import Bot
from aiogram.types import CallbackQuery, FSInputFile
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from pytz import timezone
from taskiq.scheduler.created_schedule import CreatedSchedule
from taskiq_redis import RedisScheduleSource

from pupa.bot.enums import PupaState
from pupa.bot.states.dialog_states import CareStates, MainMenuState
from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository
from pupa.infrastructure.scheduler.tasks import rest_pupa, bad_task


@inject
async def on_start_rest(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource]
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']
	await repository.pupa.set_decrease_values(
		pupa_id=pupa.id,
		mood=0,
		hungry=1
	)
	await repository.pupa.set_state(pupa_id=pupa.id, state=PupaState.rest)
	schedule_rest: CreatedSchedule = await rest_pupa.schedule_by_cron(
		source=redis_source,
		cron='*/2 * * * *',
		pupa_id=pupa.id
	)
	audio_message = await bot.send_audio(
		audio=FSInputFile('resources/media/audio/chil.mp3'),
		chat_id=callback.from_user.id
	)
	dialog_manager.dialog_data['schedule_rest_id'] = schedule_rest.schedule_id
	dialog_manager.dialog_data['audio_message_id'] = audio_message.message_id

	await dialog_manager.switch_to(state=CareStates.rest)


@inject
async def on_stop_rest(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource]
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']
	schedule_rest_id = dialog_manager.dialog_data['schedule_rest_id']

	await repository.pupa.set_state(pupa_id=pupa.id, state=PupaState.nothing)
	await redis_source.delete_schedule(schedule_rest_id)
	await repository.pupa.set_decrease_values(
		pupa_id=pupa.id,
		mood=0,
		hungry=1
	)
	await bot.delete_message(chat_id=callback.from_user.id, message_id=dialog_manager.dialog_data['audio_message_id'])
	await dialog_manager.start(state=MainMenuState.main_menu, mode=StartMode.RESET_STACK)


@inject
async def on_eat(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource]
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']

	await repository.pupa.set_state(pupa_id=pupa.id, state=PupaState.eat)
	await repository.pupa.inscribe_hungry(pupa_id=pupa.id, value=30)
	if pupa.schedule_food_id:
		await redis_source.delete_schedule(pupa.schedule_food_id)
	schedule_bad: CreatedSchedule = await bad_task.schedule_by_time(
		source=redis_source,
		time=datetime.now(tz=timezone('Europe/Moscow')) + timedelta(minutes=30),
		pupa_id=pupa.id,
		chat_id=dialog_manager.event.from_user.id
	)
	pupa.schedule_food_id = schedule_bad.schedule_id
	await repository.pupa.set_schedule_food_id(pupa_id=pupa.id, schedule_id=schedule_bad.schedule_id)
	dialog_manager.dialog_data['food_media'] = True
	await dialog_manager.show()
	await sleep(3)
	await dialog_manager.start(state=MainMenuState.main_menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)

