import asyncio
from dataclasses import dataclass
from datetime import datetime

import asyncpg
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from asyncpg import Connection


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

	for p in pupas:
		pupa = Pupa(**p)
		if pupa.sleep_state:
			continue

		if pupa.hungry == 31:
			async with Bot('7685151745:AAEswltJ1CgGVkP3YApSGalNYa2VUZ2ktos') as bot:
				chat_id = await conn.fetch("SELECT tg_user_id FROM users WHERE id = $1", pupa.owner_id)
				await bot.send_message(
					chat_id=chat_id[0]['tg_user_id'],
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