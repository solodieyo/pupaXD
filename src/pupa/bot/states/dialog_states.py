from aiogram.fsm.state import StatesGroup, State


class MainMenuState(StatesGroup):
	main_menu = State()


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
