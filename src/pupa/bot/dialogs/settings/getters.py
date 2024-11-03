from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.config import AppConfig
from pupa.infrastructure.db.models import User


@inject
async def getter_settings(
	dialog_manager: DialogManager,
	user: User,
	config: FromDishka[AppConfig],
	**_,
):
	return {
		'admin': True if user.tg_user_id in config.tg.admins_id else False
	}