from aiogram.types import ErrorEvent


async def error_handler(event: ErrorEvent):
	await event.update.callback_query.message.delete()