from aiogram import Bot
from aiogram.types import Message
from aiogram_dialog.manager.message_manager import SEND_METHODS

from app.src.bot.sender.new_message_modal import NewMessage


async def send_message(bot: Bot, new_message: NewMessage) -> Message:
	if new_message.media_id:
		return await _send_media(bot, new_message)
	else:
		return await _send_text(bot, new_message)


async def _send_text(bot: Bot, new_message: NewMessage) -> Message:
	message = await bot.send_message(
		chat_id=new_message.chat_id,
		text=new_message.text,
		disable_notification=new_message.disable_notification,
		reply_markup=new_message.reply_markup,
		parse_mode=new_message.parse_mode,
	)

	if new_message.poll_tittle:
		await _send_poll(bot, new_message)

	return message


async def _send_poll(bot: Bot, new_message: NewMessage):
	await bot.send_poll(
		chat_id=new_message.chat_id,
		question=new_message.poll_tittle,
		options=new_message.poll_options
	)


async def _send_media(bot: Bot, new_message: NewMessage) -> Message:
	method = getattr(bot, SEND_METHODS[new_message.media_content_type], None)
	if not method:
		raise ValueError(f"ContentType {new_message.media_content_type} is not supported")
	message = await method(
		new_message.chat_id,
		new_message.media_id,
		caption=new_message.text,
		reply_markup=new_message.reply_markup,
		parse_mode=new_message.parse_mode,
		has_spoiler=new_message.hide_media
	)

	if new_message.poll_tittle:
		await _send_poll(bot, new_message)

	return message
