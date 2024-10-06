from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka

from pupa.config import AppConfig

router = Router()


@router.message(Command('issue'))
async def issue_command(
	message: Message,
	command: CommandObject,
	bot: Bot,
	config: FromDishka[AppConfig]
):
	if command.args:
		await bot.send_message(
			chat_id=config.tg.idea_channel_id,
			text='<b>Новое предложение!</b>\n\n'
				 f'От пользователя - {message.from_user.full_name} '
		)
