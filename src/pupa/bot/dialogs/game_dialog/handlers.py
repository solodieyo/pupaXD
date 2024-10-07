import time

from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode, ShowMode
from aiogram_dialog.widgets.kbd import Button
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject
from taskiq.scheduler.created_schedule import CreatedSchedule
from taskiq_redis import RedisScheduleSource

from pupa.bot.enums import PupaState
from pupa.bot.enums.question_type import QuestionType
from pupa.bot.states.dialog_states import GameStates, MainMenuState
from pupa.infrastructure.db.models import Pupa, User
from pupa.infrastructure.db.repositories import GeneralRepository
from pupa.infrastructure.scheduler.tasks import self_education_task


@inject
async def on_learn_with_pupa(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']
	check = await check_pupa_status(pupa=pupa, callback=callback)
	if check:
		await dialog_manager.switch_to(state=GameStates.learn_with_pupa)


@inject
async def on_pupa_self_education(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource]
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']
	check = await check_pupa_status(pupa=pupa, callback=callback)
	if check:
		await repository.pupa.set_state(pupa_id=pupa.id, state=PupaState.education)
		schedule_education: CreatedSchedule = await self_education_task.schedule_by_cron(
			source=redis_source,
			cron='*/3 * * * *',
			pupa_id=pupa.id
		)
		dialog_manager.dialog_data['schedule_education_id'] = schedule_education.schedule_id
		await dialog_manager.switch_to(state=GameStates.pupa_self_education, show_mode=ShowMode.EDIT)


@inject
async def on_stop_self_education(
	callback: CallbackQuery,
	widget: Button,
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	redis_source: FromDishka[RedisScheduleSource]
):
	pupa: Pupa = dialog_manager.middleware_data['pupa']
	schedule_education_id = dialog_manager.dialog_data['schedule_education_id']

	await repository.pupa.set_state(pupa_id=pupa.id, state=PupaState.nothing)
	await redis_source.delete_schedule(schedule_education_id)
	await dialog_manager.start(state=MainMenuState.main_menu, mode=StartMode.RESET_STACK)


async def check_pupa_status(pupa: Pupa, callback: CallbackQuery):
	if pupa.hungry < 60:
		await callback.answer('Пупа слишком голодная чтобы учится.', show_alert=True)
		return False
	elif pupa.mood < 50:
		await callback.answer('Пупа не в духе чтобы учится.', show_alert=True)
		return False
	return True


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

	if time.time() - start_time > 2:
		await callback.answer('Слишком долго(')

	elif selected_item == dialog_manager.dialog_data['answer']:
		dialog_manager.dialog_data['true_answers'] += 1
		await repository.questions.user_correct_answer_question(
			user_id=user.id,
			question_id=dialog_manager.dialog_data['question_id'],
			count_answers=dialog_manager.dialog_data.get('count_user_answers', 0),
			question_type=QuestionType.paints
		)
		await callback.answer('Верно!')
	else:
		await callback.answer('Неверно(')

	if dialog_manager.dialog_data['count_answers'] == 10:
		await _final_game(
			dialog_manager=dialog_manager,
			user_id=user.id,
			pupa_id=pupa.id,
			repository=repository
		)
		await dialog_manager.switch_to(GameStates.final_game)


async def _final_game(
	dialog_manager: DialogManager,
	user_id: int,
	pupa_id: int,
	repository: GeneralRepository,
):

	if dialog_manager.dialog_data['true_answers'] >= 5:
		dialog_manager.dialog_data['win'] = True

		await repository.pupa.inscribe_mood(
			pupa_id=pupa_id,
			value=abs(-4 + dialog_manager.dialog_data['true_answers'])
		)
	else:
		dialog_manager.dialog_data['win'] = False
		await repository.pupa.decrease_mood_game(
			pupa_id=pupa_id,
			value=abs(5 - dialog_manager.dialog_data['true_answers'])
		)