import asyncio
from asyncio import sleep

from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError, TelegramBadRequest
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager, ShowMode, StartMode
from aiogram_dialog.manager.message_manager import SEND_METHODS
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.bot.states.dialog_states import AdminMenuStates
from pupa.bot.utils.message_misc import FileInfo, get_file_info
from pupa.infrastructure.db.models import User
from pupa.infrastructure.db.repositories.general_repository import GeneralRepository

TASKS = set()


@inject
async def on_select_theme(
	_,
	__,
	dialog_manager: DialogManager,
	selected_item: int,
):
	dialog_manager.find('questions_scroll').set_page(page=0)
	dialog_manager.dialog_data['theme_id'] = selected_item
	await dialog_manager.switch_to(state=AdminMenuStates.manage_theme)


@inject
async def on_delete_theme(
	callback: CallbackQuery,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	await repository.theme.delete_theme(theme_id=dialog_manager.dialog_data['theme_id'])
	await callback.answer('Тема успешно удалена')
	await dialog_manager.switch_to(state=AdminMenuStates.themes_select)


@inject
async def on_input_theme_name(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	await message.delete()
	await repository.theme.create_theme(
		theme_name=message.text
	)

	await dialog_manager.switch_to(
		state=AdminMenuStates.themes_select,
		show_mode=ShowMode.EDIT
	)


async def on_select_question(
	_,
	__,
	dialog_manager: DialogManager,
	selected_item: int,
):
	dialog_manager.dialog_data['question_id'] = selected_item
	await dialog_manager.switch_to(state=AdminMenuStates.manage_question)


@inject
async def on_delete_question(
	callback: CallbackQuery,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	await repository.questions.delete_question(
		question_id=dialog_manager.dialog_data['question_id']
	)
	await callback.answer('Вопрос успешно удален')
	await dialog_manager.switch_to(state=AdminMenuStates.manage_theme_questions)


@inject
async def on_change_answer(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	await message.delete()
	await repository.questions.update_question_answer(
		question_id=dialog_manager.dialog_data['question_id'],
		answer=message.text
	)
	await dialog_manager.switch_to(
		state=AdminMenuStates.manage_question,
		show_mode=ShowMode.EDIT
	)


@inject
async def on_change_question_text(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	await message.delete()
	await repository.questions.update_question_text(
		question_id=dialog_manager.dialog_data['question_id'],
		question=message.text
	)
	await dialog_manager.switch_to(
		state=AdminMenuStates.manage_question,
		show_mode=ShowMode.EDIT
	)


@inject
async def on_change_question_media_and_text(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	file_info: FileInfo = get_file_info(message)

	await message.delete()
	await repository.questions.update_question_media_and_text(
		question_id=dialog_manager.dialog_data['question_id'],
		question=message.caption,
		media=file_info.file_id,
		content_type=file_info.content_type
	)
	await dialog_manager.switch_to(
		state=AdminMenuStates.manage_question,
		show_mode=ShowMode.EDIT
	)


@inject
async def on_change_question_media(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	file_info: FileInfo = get_file_info(message)

	await message.delete()
	await repository.questions.update_question_media(
		question_id=dialog_manager.dialog_data['question_id'],
		media=file_info.file_id,
		content_type=file_info.content_type
	)
	await dialog_manager.switch_to(
		state=AdminMenuStates.manage_question,
		show_mode=ShowMode.EDIT
	)


async def on_create_question_text(
	message: Message,
	__,
	dialog_manager: DialogManager,
):
	await message.delete()
	dialog_manager.dialog_data['question_text'] = message.text
	await dialog_manager.switch_to(
		state=AdminMenuStates.add_question_answer,
		show_mode=ShowMode.EDIT
	)


async def on_create_question_media(
	message: Message,
	__,
	dialog_manager: DialogManager,
):
	await message.delete()
	file_info: FileInfo = get_file_info(message)
	dialog_manager.dialog_data.update(
		question_media=file_info.file_id,
		question_media_type=file_info.content_type,
		question_text=message.caption
	)
	await dialog_manager.switch_to(
		state=AdminMenuStates.add_question_answer,
		show_mode=ShowMode.EDIT
	)


@inject
async def on_create_question_answer(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	await message.delete()
	await repository.questions.add_question(
		theme_id=dialog_manager.dialog_data['theme_id'],
		question=dialog_manager.dialog_data.get('question_text'),
		media=dialog_manager.dialog_data.get('question_media'),
		media_content_type=dialog_manager.dialog_data.get('question_media_type'),
		answer=message.text,
	)

	dialog_manager.dialog_data.update(
		question_text=None,
		question_media=None,
		question_media_type=None,
		answer=None
	)

	await dialog_manager.switch_to(
		state=AdminMenuStates.manage_theme_questions,
		show_mode=ShowMode.EDIT,
	)
	await message.answer(
		'Вопрос успешно добавлен',
		reply_markup=InlineKeyboardMarkup(
			inline_keyboard=[
				[InlineKeyboardButton(
					text='Закрыть',
					callback_data='delete_message'
				)]]
		)
	)


@inject
async def on_mailing(
	message: Message,
	__,
	dialog_manager: DialogManager,
	repo: FromDishka[GeneralRepository],
	bot: FromDishka[Bot],
):
	users = await repo.user.get_users()
	task = asyncio.create_task(
		_mailing(
			users=users,
			bot=bot,
			message=message)
	)
	TASKS.add(task)
	await message.answer('Рассылка началась')
	await dialog_manager.start(
		state=AdminMenuStates.mailing,
		show_mode=ShowMode.EDIT,
		mode=StartMode.RESET_STACK
	)


async def _mailing(
	users: list[User],
	bot: Bot,
	message: Message
):
	if message.text:
		await _send_text(
			bot=bot,
			text=message.text,
			users=users
		)
	else:
		await _send_media(
			bot=bot,
			message=message,
			file_id=get_file_id(message),
			users=users
		)


def get_file_id(message: Message):
	if message.photo:
		return message.photo[-1].file_id
	elif message.document:
		return message.document.file_id


async def _send_text(
	bot: Bot,
	text: str,
	users: list[User],
):
	for user in users:
		try:
			await bot.send_message(
				chat_id=user.tg_user_id,
				text=text,
			)
		except (TelegramForbiddenError, TelegramBadRequest):
			continue


async def _send_media(
	bot: Bot,
	message: Message,
	file_id: str,
	users: list[User],
):
	method = getattr(bot, SEND_METHODS[message.content_type], None)
	if not method:
		raise ValueError(
			f"ContentType {message.content_type} is not supported",
		)
	for user in users:
		try:
			await method(
				chat_id=user.tg_user_id,
				media=file_id,
				caption=message.caption,
			)
			await sleep(1)
		except (TelegramForbiddenError, TelegramBadRequest):
			continue
