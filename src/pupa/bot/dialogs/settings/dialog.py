from aiogram import F
from aiogram.enums import ContentType
from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import SwitchTo, Row, Start
from aiogram_dialog.widgets.text import Const

from pupa.bot.dialogs.settings.getters import getter_settings
from pupa.bot.dialogs.settings.handlers import input_sleep_time, input_issue
from pupa.bot.states.dialog_states import SettingsStates, AdminMenuStates

setting_menu = Window(
	Const('qwe'),
	Row(
		SwitchTo(
			text=Const('🛏 Время Сна'),
			state=SettingsStates.sleep_time,
			id='sleep_time'
		),
		SwitchTo(
			text=Const('💌 Написать пупе'),
			state=SettingsStates.issue,
			id='issue'
		)
	),
	Start(
		text=Const('🅰️ Админ меню'),
		state=AdminMenuStates.main,
		id='admin_menu',
		when=F['admin'].is_(True)
	),
	state=SettingsStates.main,
	getter=getter_settings

)

change_sleep_time = Window(
	Const('Здесь вы можете изменить время сна для Пупы, время отсчитывается по Москве.'),
	Const(
		'<b>Некорректный формат времени. Отправьте, пожалуйста, время в корректном формате.</b>',
		when=F['dialog_data']['wrong_time']
	),
	Const('Введите в какое время Пупе ложится спать?\n\n'
		  'В формате:\n<blockquote>"18:30", "18 30", "1830"</blockquote>'),
	MessageInput(
		func=input_sleep_time,
		content_types=ContentType.TEXT
	),
	Start(
		text=Const('Назад'),
		state=SettingsStates.main,
		id='back_to_main',
		mode=StartMode.RESET_STACK
	),
	state=SettingsStates.sleep_time,
)

issue = Window(
	Const(
		'<b>Ваше предложение отправлено!\n</b>',
		when=F['dialog_data']['sent'].is_(True)
	),
	Const('💡 Здесь вы можете предложить свою идею по улучшению нашего бота'),
	MessageInput(
		func=input_issue,
		content_types=ContentType.TEXT
	),
	Start(
		text=Const('Назад'),
		state=SettingsStates.main,
		id='back_to_main',
		mode=StartMode.RESET_STACK
	),
	state=SettingsStates.issue,
)


settings_dialog = Dialog(
	setting_menu,
	change_sleep_time,
	issue
)