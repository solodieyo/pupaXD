from aiogram import Bot
from aiogram.filters import BaseFilter


class LengthFilter(BaseFilter):
	async def __call__(self, message, bot: Bot):
		if len(message.text) > 21:
			await bot.send_message(chat_id=message.chat.id, text='Ответ слишком длинный.')
			return False
		return True
