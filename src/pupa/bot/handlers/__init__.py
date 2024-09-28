from aiogram import Router

from .start import router as start_router
from .callback.pupa_poop import router as callback_router


def setup_routers():
	router = Router()
	router.include_routers(
		start_router,
		callback_router
	)
	return router