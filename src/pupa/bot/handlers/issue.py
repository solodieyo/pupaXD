from aiogram import Router, Bot
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from dishka import FromDishka
from dishka.integrations.aiogram import inject

from pupa.config import AppConfig

router = Router()


@router.message(Command('issue'))
@inject
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
				 f'От пользователя - <a href="t.me/{message.from_user.username}">{message.from_user.full_name}</a>'
				 f' - <ID[<code>{message.from_user.id}</code>]\n\n'
				 f'{command.args}'
		)
		await message.reply('Ваше предложение отправлено')
	else:
		await message.answer('💡 Здесь вы можете предложить свою идею по улучшению нашего бота\n\n'
							 'Напишите "<code>/issue Текст...</code>", чтобы отправить нам сообщение.')