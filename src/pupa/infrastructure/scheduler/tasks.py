from aiogram import Bot
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton
from alembic.util import status
from dishka import FromDishka
from dishka.integrations.taskiq import inject

from pupa.infrastructure.db.models import Pupa
from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.scheduler.broker import broker


@broker.task
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


@broker.task
@inject
async def decrease_pupa_hungry(
	pupa_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	await repository.pupa.decrease_hungry(pupa_id=pupa_id)


@broker.task
@inject
async def decrease_pupa_mood(
	pupa_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	await repository.pupa.decrease_mood(pupa_id=pupa_id)


@broker.task
@inject
async def rest_pupa(
	pupa_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	await repository.pupa.inscribe_mood(pupa_id=pupa_id)


@broker.task
async def poop_task(
	pupa_id: int,
	chat_id: int,
	bot: FromDishka[Bot],
	repository: FromDishka[GeneralRepository],
):
	gif = FSInputFile('')
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
