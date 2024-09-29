from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, Dialog, StartMode
from aiogram_dialog.widgets.kbd import Row, Button, Start
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media.dynamic import DynamicMedia

from pupa.bot.dialogs.care_dialog.getters import getter_care_menu
from pupa.bot.dialogs.care_dialog.handlers import on_start_rest, on_stop_rest, on_eat
from pupa.bot.dialogs.common.getters import get_pupa_status
from pupa.bot.states.dialog_states import CareStates, MainMenuState

care_main_menu = Window(
	Format(
		text='🍞{hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}',
		when=F['food_media'].is_not(True)
	),
	DynamicMedia(
		selector='media',
	),
	Start(
		text=Const('😼 Как ты пупа?'),
		id='back_to_main',
		state=MainMenuState.main_menu,
		mode=StartMode.RESET_STACK,
		when=F['food_media'].is_not(True)
	),
	Row(
		Button(
			text=Const('🍔 Еда'),
			id='eating',
			on_click=on_eat,
			when=F['food_media'].is_not(True)
		),
		Button(
			text=Const('🛏️ Отдых'),
			id='chill',
			on_click=on_start_rest,
			when=F['food_media'].is_not(True)
		),
	),
	state=CareStates.care_menu,
	getter=(
		get_pupa_status,
		getter_care_menu
	)
)

rest_window = Window(
	StaticMedia(
		path='resources/media/gifs/chill.gif',
		type=ContentType.DOCUMENT
	),
	Button(
		text=Const('Перестать отдыхать'),
		id='rest_pause',
		on_click=on_stop_rest
	),
	state=CareStates.rest,
	getter=(
		get_pupa_status,
	)
)

care_dialog = Dialog(
	care_main_menu,
	rest_window
)
