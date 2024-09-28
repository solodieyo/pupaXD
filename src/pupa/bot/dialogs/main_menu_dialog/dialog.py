from aiogram_dialog import Window, Dialog, ShowMode
from aiogram_dialog.widgets.kbd import Start, Row, Button
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format

from pupa.bot.dialogs.common.getters import get_pupa_status, get_main_media
from pupa.bot.dialogs.main_menu_dialog.handlers import on_how_pupa
from pupa.bot.states.dialog_states import MainMenuState, CareStates, GameStates

main_window = Window(
	Format(
		text='🍞{hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	DynamicMedia(
		selector='main_media'
	),
	Button(
		text=Const('🏫 Как ты пупа?'),
		id='how_pupa',
		on_click=on_how_pupa
	),
	Row(
		Start(
			text=Const('🏡 Забота'),
			id='care_start',
			state=CareStates.care_menu,
			show_mode=ShowMode.EDIT
		),
		Start(
			text=Const('⛳️ Игра'),
			id='game_start',
			state=GameStates.game_menu,
			show_mode=ShowMode.EDIT
		)
	),
	state=MainMenuState.main_menu,
	getter=(get_main_media, get_pupa_status)
)

menu_dialog = Dialog(
	main_window
)
