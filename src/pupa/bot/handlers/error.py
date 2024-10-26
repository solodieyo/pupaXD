from aiogram.exceptions import TelegramBadRequest
from aiogram.types import ErrorEvent


async def error_handler(event: ErrorEvent):
	try:
		await event.update.callback_query.message.delete()
	except TelegramBadRequest:
		return