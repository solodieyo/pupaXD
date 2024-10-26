from aiogram import Router

from .start import router as start_router
from .issue import router as issue_router
from .callback.sleep import router as sleep_router
from .callback.pupa_poop import router as callback_router
from .callback.eat import router as eat_router


def setup_routers():
	router = Router()
	router.include_routers(
		start_router,
		callback_router,
		sleep_router,
		issue_router,
		eat_router
	)
	return router