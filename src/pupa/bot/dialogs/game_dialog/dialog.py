from aiogram import F
from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Start, Button, Select, Group
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from pupa.bot.dialogs.common.getters import get_pupa_status
from pupa.bot.dialogs.game_dialog.getters import journey_game_getter, getter_question_id
from pupa.bot.dialogs.game_dialog.handlers import os_select_theme, on_question_click
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
			text=Const('🏫 Пупа самоучка'),
			id='self_education',
			state=GameStates.pupa_self_education
		),
	),
	Row(
		SwitchTo(
			text=Const('🏡 Приключение'),
			id='care_start',
			state=GameStates.pupa_journey_select_theme
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

# СДЕЛАТЬ ВЫБОР ТЕМЫ ЧЕРЕЗ СЕЛЕКТ GROUP С ЕНУМАМИ
journey_select_theme = Window(
	Const('<b>Для начала приключения, выбери интересную тему!</b>'),
	Button(
		text=Const('Картины'),
		id='pictures',
		on_click=os_select_theme
	),
	SwitchTo(
		text=Const('Я передумал..'),
		state=GameStates.game_menu,
		id='__back__',
	),
	state=GameStates.pupa_journey_select_theme,
)


journey_game = Window(
	Format(
		text='{game_text}'
	),
	DynamicMedia(
		selector='game_media',
		when=F['has_media'].is_(True)
	),
	Group(
		Select(
			text=Format('{item}'),
			id='question_select',
			item_id_getter=getter_question_id,
			items='questions',
			on_click=on_question_click,
			type_factory=str
		),
		width=2
	),
	state=GameStates.pupa_journey,
	getter=journey_game_getter
)