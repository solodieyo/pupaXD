from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Start, Button, Group, Select
from aiogram_dialog.widgets.media import StaticMedia, DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from pupa.bot.dialogs.common.getters import get_pupa_status, get_main_media
from pupa.bot.dialogs.game_dialog.getters import (
	journey_game_getter,
	getter_question_id,
	getter_final_menu
)
from pupa.bot.dialogs.game_dialog.handlers import (
	on_pupa_self_education,
	on_stop_self_education,
	on_question_click,
	os_select_theme
)
from pupa.bot.states.dialog_states import GameStates, MainMenuState

game_main_menu = Window(
	Format(
		text='🍞{hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	DynamicMedia(
		selector='main_media'
	),
	Start(
		text=Const('😼 Как ты Пупа?'),
		id='back_to_main',
		state=MainMenuState.main_menu,
		mode=StartMode.RESET_STACK
	),
	Row(
		SwitchTo(
			text=Const('🖌️ Приключение с Пупой'),
			id='journey_start',
			state=GameStates.pupa_journey_select_theme
		),
		Button(
			text=Const('🏫 Пупа самоучка'),
			id='self_education',
			on_click=on_pupa_self_education
		),
	),
	state=GameStates.game_menu,
	getter=(get_main_media, get_pupa_status)
)

pupa_self_education = Window(
	StaticMedia(
		path=Const('resources/media/gifs/self_education.gif'),
		type=ContentType.DOCUMENT
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
	DynamicMedia(
		selector='main_media'
	),
	Button(
		text=Const('Картины'),
		id='pictures',
		on_click=os_select_theme
	),
	SwitchTo(
		text=Const('Не хочу учиться'),
		state=GameStates.game_menu,
		id='__back__',
	),
	state=GameStates.pupa_journey_select_theme,
	getter=get_main_media
)

journey_game = Window(
	Format(
		text='{game_text}'
	),
	Format(
		text="Вопрос {question_number} из 10"
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

game_final_menu = Window(
	Const('<b>Конец приключения</b>\n'),
	Format(
		text='{final_text}'
	),
	DynamicMedia(
		selector='final_media'
	),
	Start(
		text=Const('Вернуться домой'),
		state=MainMenuState.main_menu,
		id='__back_to_main__'
	),
	state=GameStates.final_game,
	getter=getter_final_menu
)

game_dialog = Dialog(
	game_main_menu,
	pupa_self_education,
	journey_select_theme,
	journey_game,
	game_final_menu
)
