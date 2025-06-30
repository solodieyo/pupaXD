from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
	main_menu = State()
	time_menu = State()
	sleep = State()


class CareStates(StatesGroup):
	care_menu = State()
	food = State()
	rest = State()


class GameStates(StatesGroup):
	game_menu = State()
	learn_with_pupa = State()
	pupa_self_education = State()
	pupa_journey_select_theme = State()
	pupa_journey = State()
	final_game = State()


class SettingsStates(StatesGroup):
	main = State()
	sleep_time = State()
	issue = State()


class AdminMenuStates(StatesGroup):
	main = State()
	stats = State()
	themes_select = State()
	add_theme = State()
	manage_theme = State()
	manage_theme_questions = State()
	delete_theme_confirm = State()
	manage_question = State()
	delete_question_confirm = State()
	change_answer = State()
	change_question = State()
	add_question = State()
	add_question_answer = State()
	change_media = State()
	mailing = State()


class StatisticStates(StatesGroup):
	main = State()