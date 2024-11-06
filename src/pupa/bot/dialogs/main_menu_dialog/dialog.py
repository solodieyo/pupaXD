from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start, Row, Button
from aiogram_dialog.widgets.media import DynamicMedia, StaticMedia
from aiogram_dialog.widgets.text import Const, Format

from pupa.bot.dialogs.common.getters import get_pupa_status, get_main_media
from pupa.bot.dialogs.common.handlers import ignore
from pupa.bot.dialogs.main_menu_dialog.handlers import on_how_pupa, on_game_start, input_sleep_time, on_wake_up
from pupa.bot.states.dialog_states import MainMenuState, CareStates, SettingsStates

time_window = Window(
	Const(
		'<b>Некорректный формат времени. Отправьте, пожалуйста, время в корректном формате.</b>',
		when=F['dialog_data']['wrong_time']
	),
	Const('Введите в какое время Пупе ложится спать? (По Мск.)\n\n'
		  'В формате:\n<blockquote>"18:30", "18 30", "1830"</blockquote>'),
	MessageInput(
		func=input_sleep_time,
		content_types=ContentType.TEXT
	),
	state=MainMenuState.time_menu
)

main_window = Window(
	Format(
		text='🍔{hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
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
		Button(
			text=Const('⛳️ Игра'),
			id='game_start',
			on_click=on_game_start
		)
	),
	MessageInput(
		func=ignore,
	),
	state=MainMenuState.main_menu,
	getter=(get_main_media, get_pupa_status)
)

sleep_window = Window(
	StaticMedia(
		path='resources/media/gifs/sleep.gif',
		type=ContentType.DOCUMENT
	),
	MessageInput(
		func=ignore,
	),
	Button(
		text=Const('Разбудить Пупу'),
		id='wake_up',
		on_click=on_wake_up
	),
	state=MainMenuState.sleep
)


menu_dialog = Dialog(
	time_window,
	main_window,
	sleep_window
)
