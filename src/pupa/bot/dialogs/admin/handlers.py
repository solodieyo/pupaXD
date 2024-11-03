from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.bot.states.dialog_states import AdminMenuStates
from pupa.bot.utils.message_misc import FileInfo, get_file_info
from pupa.infrastructure.db.repositories import GeneralRepository


@inject
async def on_select_theme(
	_,
	__,
	dialog_manager: DialogManager,
	selected_item: int,
):
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
	await dialog_manager.switch_to(state=AdminMenuStates.manage_theme)


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
	await dialog_manager.switch_to(state=AdminMenuStates.manage_question)


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
	await dialog_manager.switch_to(state=AdminMenuStates.manage_question)


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
	await dialog_manager.switch_to(state=AdminMenuStates.manage_question)


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
	await dialog_manager.switch_to(state=AdminMenuStates.manage_question)


async def on_create_question_text(
	message: Message,
	__,
	dialog_manager: DialogManager,
):
	await message.delete()
	dialog_manager.dialog_data['question_text'] = message.text
	await dialog_manager.switch_to(state=AdminMenuStates.add_question_answer)


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
	await dialog_manager.switch_to(state=AdminMenuStates.add_question_answer)


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
		question=dialog_manager.dialog_data['question_text'],
		media=dialog_manager.dialog_data['question_media'],
		content_type=dialog_manager.dialog_data['question_media_type'],
		answer=message.text,
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
