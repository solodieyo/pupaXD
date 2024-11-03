from aiogram_dialog import DialogManager
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from pupa.infrastructure.db.repositories import GeneralRepository


@inject
async def getter_statistic_main(
	dialog_manager: DialogManager,
	repository: FromDishka[GeneralRepository],
	**_,
):
	return {
		'count_users': await repository.stats.get_user_count(),
		'count_today': await repository.stats.get_user_count_day(),
		'count_week': await repository.stats.get_user_count_week(),
		'count_month': await repository.stats.get_user_count_month(),
	}
