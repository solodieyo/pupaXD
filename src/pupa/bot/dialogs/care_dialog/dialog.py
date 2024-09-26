from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Row, SwitchTo, Button
from aiogram_dialog.widgets.media import StaticMedia
from aiogram_dialog.widgets.text import Format, Const
from aiogram_dialog.widgets.media.dynamic import DynamicMedia

from pupa.bot.dialogs.care_dialog.handlers import on_start_rest, on_stop_rest, on_eat
from pupa.bot.dialogs.common.getters import get_pupa_status
from pupa.bot.dialogs.common.widgets import BACK_TO_MAIN_MENU, BACK_TO_CARE_MENU
from pupa.bot.states.dialog_states import CareStates

care_main_menu = Window(
	Format(
		text='🍞 {hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	StaticMedia(
		path=Const('resources/media/images/test.png'),
	),
	Row(
		SwitchTo(
			text=Const('🍔 Еда'),
			id='care_start',
			state=CareStates.food
		),
		Button(
			text=Const('🛏️ Отдых'),
			id='game_start',
			on_click=on_start_rest
		),
		BACK_TO_MAIN_MENU
	),
	state=CareStates.care_menu,
	getter=get_pupa_status
)

food_window = Window(
	Format(
		text='🍞 {hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	DynamicMedia(
		selector='food_media',
	),
	Button(
		text=Const('Бургер'),
		id='food_burger',
		on_click=on_eat
	),
	BACK_TO_CARE_MENU,
	state=CareStates.food,
	getter=(
		get_pupa_status,
		getter_food_media
	)
)	

rest_window = Window(
	Format(
		text='🍞 {hungry}% | {hungry_state}\n🤗{mood}% | {mood_state}'
	),
	StaticMedia(
		path=Const('')
	),
	Button(
		text=Const('Перестать отдыхать'),
		id='rest_pause',
		on_click=on_stop_rest
	),
	state=CareStates.rest,
	getter=get_pupa_status
)