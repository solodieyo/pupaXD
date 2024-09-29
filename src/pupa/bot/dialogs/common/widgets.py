from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from pupa.bot.states.dialog_states import MainMenuState, CareStates

BACK_TO_MAIN_MENU = Start(
	text=Const('Как ты Пупа?'),
	id='__main_menu__',
	state=MainMenuState.main_menu,
	mode=StartMode.RESET_STACK
)


BACK_TO_CARE_MENU = Start(
	text=Const('Назад'),
	id='__care_menu__',
	state=CareStates.care_menu,
	mode=StartMode.RESET_STACK
)