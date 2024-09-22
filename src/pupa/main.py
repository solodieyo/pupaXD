import asyncio

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs

from pupa.factory.main_factory import get_dishka, get_config
from pupa.factory.setup_log import setup_logging


async def main():
	setup_logging()
	config = get_config()
	dishka = get_dishka(config)

	bot: Bot = await dishka.get(Bot)
	dp: Dispatcher = await dishka.get(Dispatcher)
	setup_dialogs(dp)

	dp['dishka_container'] = dishka

	await bot.delete_webhook(drop_pending_updates=True)
	await dp.start_polling(bot)


if __name__ == '__main__':
	asyncio.run(main())