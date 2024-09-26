import time

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.bot.enums.question_type import QuestionType
from pupa.bot.states.dialog_states import GameStates
from pupa.infrastructure.db.models import User, Pupa
from pupa.infrastructure.db.repositories import GeneralRepository


@inject
async def os_select_theme(
	_,
	__,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	user: User = dialog_manager.middleware_data['user']
	dialog_manager.dialog_data.update(
		game_text='<b>Кто автор этой картины?</b>',
		has_media=True,
		game_type=QuestionType.paints,
		count_answers=0,
		true_answers=0
	)
	await dialog_manager.switch_to(GameStates.pupa_journey)


@inject
async def on_question_click(
	callback: CallbackQuery,
	__,
	dialog_manager: DialogManager,
	selected_item: str,
	repository: FromDishka[GeneralRepository],
):
	user: User = dialog_manager.middleware_data['user']
	pupa: Pupa = dialog_manager.middleware_data['pupa']

	dialog_manager.dialog_data['count_answers'] += 1
	start_time = dialog_manager.dialog_data['start_time']

	if time.time() - start_time > 10 + pupa.

	if selected_item == dialog_manager.dialog_data['answer']:
		dialog_manager.dialog_data['true_answers'] += 1
		await repository.questions.user_correct_answer_question(
			user_id=user.id,
			question_id=dialog_manager.dialog_data['question_id'],
			count_answers=dialog_manager.dialog_data.get('count_user_answers', 0)
		)
		await callback.answer('Верно!')

	if dialog_manager.dialog_data['count_answers'] == 10:
		await dialog_manager.switch_to(GameStates.final_game)


