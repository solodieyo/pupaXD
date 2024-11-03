from aiogram import Router

from .main_menu_dialog.dialog import menu_dialog
from .care_dialog.dialog import care_dialog
from .game_dialog.dialog import game_dialog
from .settings.dialog import settings_dialog
from .admin.dialog import admin_dialog
from .statistic.dialog import statistic_dialog


def include_dialogs():
	router = Router()
	router.include_routers(
		menu_dialog,
		care_dialog,
		game_dialog,
		settings_dialog,
		admin_dialog,
		statistic_dialog
	)
	return router
