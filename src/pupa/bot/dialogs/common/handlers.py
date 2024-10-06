from aiogram_dialog import ShowMode, DialogManager


async def ignore(_, __, dialog_manager: DialogManager):
	dialog_manager.show_mode = ShowMode.NO_UPDATE