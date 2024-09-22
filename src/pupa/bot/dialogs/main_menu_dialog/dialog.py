from aiogram_dialog import Window, Dialog
from aiogram_dialog.widgets.kbd import Start, Row
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from pupa.bot.dialogs.common.getters import get_pupa_status
from pupa.bot.states.dialog_states import MainMenuState, CareStates, GameStates

main_window = Window(
	Format(
		text='🍞 {hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	StaticMedia(
		path=Const('resources/media/images/test.png'),
	),
	Row(
		Start(
			text=Const('🏡 Забота'),
			id='care_start',
			state=CareStates.care_menu
		),
		Start(
			text=Const('⛳️ Игра'),
			id='game_start',
			state=GameStates.game_menu
		)
	),
	state=MainMenuState.main_menu,
	getter=get_pupa_status
)


menu_dialog = Dialog(
	main_window
)