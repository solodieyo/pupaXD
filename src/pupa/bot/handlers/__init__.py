from aiogram import Router

from .start import router as start_router


def setup_routers():
	router = Router()
	router.include_routers(
		start_router,
	)
	return router