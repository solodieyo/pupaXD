from aiogram_dialog import DialogManager, ShowMode

from pupa.bot.states.dialog_states import MainMenuState


async def on_how_pupa(
	_,
	__,
	dialog_manager: DialogManager
):
	await dialog_manager.show(
		show_mode=ShowMode.EDIT
	)