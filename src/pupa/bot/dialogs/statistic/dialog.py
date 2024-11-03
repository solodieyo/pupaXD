from aiogram_dialog import Window, StartMode, Dialog
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format, Const

from pupa.bot.dialogs.statistic.getters import getter_statistic_main
from pupa.bot.states.dialog_states import AdminMenuStates, StatisticStates

statistic_main = Window(
	Const(text='📊 <b>Статистика</b>\n'),
	Format("👥 Кол-во пользователей <code>{count_users}</code>"),
	Format('└ Сегодня — +<code>{count_today}</code>'),
	Format('└ За неделю — +<code>{count_all}</code>'),
	Format('└ За месяц — +<code>{count_month}</code>'),
	Start(
		text=Const('Назад'),
		state=AdminMenuStates.main,
		id='back_to_admin',
		mode=StartMode.RESET_STACK
	),
	state=StatisticStates.main,
	getter=getter_statistic_main
)


statistic_dialog = Dialog(
	statistic_main
)