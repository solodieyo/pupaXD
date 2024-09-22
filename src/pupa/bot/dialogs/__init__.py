from aiogram import Router

from .main_menu_dialog.dialog import menu_dialog


def include_dialogs():
	router = Router()
	router.include_routers(
		menu_dialog
	)
	return router
