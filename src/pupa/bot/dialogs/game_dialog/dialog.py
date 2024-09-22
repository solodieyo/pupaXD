from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Start, Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const

from pupa.bot.dialogs.common.getters import get_pupa_status
from pupa.bot.states.dialog_states import GameStates, MainMenuState

game_main_menu = Window(
	Format(
		text='🍞 {hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	StaticMedia(
		path=Const('resources/media/images/test.png'),
	),
	Row(
		SwitchTo(
			text=Const('📚 Учится с пупой'),
			id='lear_with_pupa',
			state=GameStates.learn_with_pupa
		),
		SwitchTo(
			text=Const('🏫 Пупа самоучка'),
			id='self_education',
			state=GameStates.pupa_self_education
		),
	),
	Row(
		SwitchTo(
			text=Const('🏡 Забота'),
			id='care_start',
			state=GameStates.pupa_journey
		),
		Start(
			text=Const('😼 Как ты пупа?'),
			id='back_to_main',
			state=MainMenuState.main_menu,
			mode=StartMode.RESET_STACK
		)
	),
	state=GameStates.game_menu,
	getter=get_pupa_status
)


pupa_self_education = Window(
	Format(
		text='🍞 {hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	StaticMedia(
		path=Const('resources/media/images/test.png'),
	),
	Button(
		text=Const('Перестать учиться'),
		id='self_education_pause',
		on_click=on_stop_self_education
	),
	state=GameStates.pupa_self_education,
	getter=get_pupa_status
)

