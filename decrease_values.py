import asyncio
from dataclasses import dataclass
from datetime import datetime

import asyncpg
from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection, Record
import logging


logging.basicConfig(
		level=logging.INFO,
		format="%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s",
	)
log = logging.getLogger(__name__)


@dataclass
class Pupa:
	id: int
	owner_id: int
	hungry: int
	mood: int
	iq: int
	decrease_food_value: int
	decrease_mood_value: int
	state: str
	poop_state: bool
	self_education_stat: int
	schedule_food_id: str
	sleep_schedule_id: str
	sleep_time: str
	sleep_state: bool
	created_at: datetime
	updated_at: datetime


async def main():

	conn: Connection = await asyncpg.connect(user="pugach", password="qweqwe", database="pupadb", host="localhost", port=5432)

	pupas = await conn.fetch("SELECT * FROM pupa")

	async with Bot('7685151745:AAEswltJ1CgGVkP3YApSGalNYa2VUZ2ktos') as bot:
		for p in pupas:
			pupa = Pupa(**p)
			if pupa.sleep_state:
				continue

			if pupa.hungry == 31:
				chat_id: Record = await conn.fetchrow("SELECT tg_user_id FROM users WHERE id = $1", pupa.owner_id)
				try:

					await bot.send_message(
						chat_id=chat_id['tg_user_id'],
						text='Пупа хочет кушать!',
						reply_markup=InlineKeyboardMarkup(
							inline_keyboard=[
								[InlineKeyboardButton(
									text='Понял, покормлю',
									callback_data=f'eat_pupa'
								)]
							]
						)
					)
					log.info("Сообщение отправлено")
				except TelegramBadRequest:
					log.error('Чат не найден')

			minus_mood = 5 if pupa.poop_state else 0
			if pupa.hungry < 30:
				minus_mood += 1
			if (pupa.mood - (pupa.decrease_mood_value + minus_mood)) >= 0:
				await conn.execute(
					"UPDATE pupa SET mood = $1 WHERE id = $2", pupa.mood - (pupa.decrease_mood_value + minus_mood), pupa.id
				)
			else:
				await conn.execute("UPDATE pupa SET mood = $1 WHERE id = $2", 0, pupa.id)

			if (pupa.hungry - pupa.decrease_food_value) >= 0:
				await conn.execute(
					"UPDATE pupa SET hungry = $1 WHERE id = $2", pupa.hungry - pupa.decrease_food_value, pupa.id
				)
			else:
				await conn.execute("UPDATE pupa SET hungry = $1 WHERE id = $2", 0, pupa.id)
	await conn.close()


if __name__ == '__main__':
	asyncio.run(main())