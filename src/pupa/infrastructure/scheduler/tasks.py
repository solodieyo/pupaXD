from aiogram import Bot
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.scheduler.broker import broker


@broker.task(task_name='self_education_task')
@inject
async def self_education_task(
	pupa_id: int,
	schedule_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	# pupa: Pupa = await repository.pupa.get_pupa_by_pupa_id(pupa_id=pupa_id)
	# if pupa.hungry < 60 or pupa.mood < 50:

	await repository.pupa.inscribe_education_time(pupa_id=pupa_id)


@broker.task(task_name='decrease_hungry')
@inject
async def decrease_hungry(
	pupa_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	await repository.pupa.decrease_hungry_(pupa_id=pupa_id)


@broker.task(task_name='decrease_mood')
@inject
async def decrease_mood(
	pupa_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	await repository.pupa.decrease_mood_(pupa_id=pupa_id)


@broker.task(task_name='rest_task')
@inject
async def rest_pupa(
	pupa_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	await repository.pupa.inscribe_mood(pupa_id=pupa_id)


@broker.task(task_name='bad_task')
@inject
async def bad_task(
	pupa_id: int,
	chat_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	gif = FSInputFile('resources/media/gifs/poop.gif')
	await bot.send_document(
		chat_id=chat_id,
		document=gif,
		reply_markup=InlineKeyboardMarkup(
			inline_keyboard=[
				[InlineKeyboardButton(
					text="Убрать",
					callback_data=f"remove_poop_{pupa_id}"
				)]
			]
		))
	await repository.pupa.set_poop_state(pupa_id=pupa_id, status=True)
	await repository.pupa.delete_schedule_food_id(pupa_id=pupa_id)