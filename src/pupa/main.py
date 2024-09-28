import asyncio
from contextlib import suppress

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from pupa.factory.main_factory import get_dishka, get_config
from pupa.factory.setup_log import setup_logging
from pupa.infrastructure.scheduler.broker import broker


async def main():
	await broker.startup()
	setup_logging()
	config = get_config()
	dishka = get_dishka(config)

	bot: Bot = await dishka.get(Bot)
	dp: Dispatcher = await dishka.get(Dispatcher)
	setup_dialogs(dp)
	setup_dishka(router=dp, container=dishka)

	dp['dishka_container'] = dishka

	try:
		await bot.delete_webhook(drop_pending_updates=True)
		await dp.start_polling(bot)
	finally:
		await dishka.close()
		await broker.shutdown()

if __name__ == '__main__':
	with suppress(KeyboardInterrupt):
		asyncio.run(main())