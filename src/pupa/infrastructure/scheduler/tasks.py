from aiogram import Bot
from dishka import FromDishka

from app.src.bot.keyboards.post_keyboard import create_post_keyboard
from app.src.bot.sender.new_message_modal import NewMessage
from app.src.bot.sender.send_message import send_message
from app.src.infrastructure.db.models import Post
from app.src.infrastructure.db.repositories import GeneralRepository
from app.src.infrastructure.scheduler.broker import broker


@broker.task
async def delay_post(
	post_id: int,
	repository: FromDishka[GeneralRepository],
	bot: FromDishka[Bot]
):
	post: Post = await repository.post.get_post_by_id(post_id=post_id)
	async with bot:
		keyboard = create_post_keyboard(
			emoji_buttons=post.emoji_buttons,
			url_buttons=post.url_buttons,
			post_id=post_id
		)
		await send_message(
			bot=bot,
			new_message=NewMessage(
				chat_id=post.channel_id,
				text=post.text,
				reply_markup=keyboard,
				media_id=post.media_id,
				media_content_type=post.media_content_type,
				hide_media=post.hide_media,
				disable_notification=post.notification
			)
		)
	await repository.post.message_sent(post_id=post_id)
