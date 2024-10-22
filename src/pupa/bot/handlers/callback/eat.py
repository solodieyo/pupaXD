from asyncio import sleep
from datetime import timedelta, datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from dishka import FromDishka
from dishka.integrations.aiogram import inject
from pytz import timezone
from taskiq.scheduler.created_schedule import CreatedSchedule
from taskiq_redis import RedisScheduleSource

from pupa.bot.enums import PupaState
from pupa.bot.states.dialog_states import CareStates, MainMenuState
from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.scheduler.tasks import bad_task

router = Router()


@router.callback_query(F.data == 'eat_pupa')
@inject
async def eat_pupa(
	callback: CallbackQuery,
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
		time=datetime.now(tz=timezone('Europe/Moscow')) + timedelta(minutes=10),
		pupa_id=pupa.id,
		chat_id=dialog_manager.event.from_user.id
	)
	pupa.schedule_food_id = schedule_bad.schedule_id
	await repository.pupa.set_schedule_food_id(pupa_id=pupa.id, schedule_id=schedule_bad.schedule_id)
	await dialog_manager.start(
		state=CareStates.food,
		mode=StartMode.RESET_STACK,
		show_mode=ShowMode.EDIT,
		data=True
	)
	await dialog_manager.show()
	await sleep(3)
	await dialog_manager.start(state=MainMenuState.main_menu, mode=StartMode.RESET_STACK, show_mode=ShowMode.EDIT)