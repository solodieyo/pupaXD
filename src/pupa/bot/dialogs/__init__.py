from aiogram import Router

from .main_menu_dialog.dialog import menu_dialog
from .care_dialog.dialog import care_dialog
from .game_dialog.dialog import game_dialog


def include_dialogs():
	router = Router()
	router.include_routers(
		menu_dialog,
		care_dialog,
		game_dialog
	)
	return router
