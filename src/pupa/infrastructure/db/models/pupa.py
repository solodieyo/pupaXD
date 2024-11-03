from datetime import datetime

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from pupa.bot.enums import PupaState
from pupa.infrastructure.db.models import Base, Int64, Int16


class Pupa(Base):
	__tablename__ = "pupa"

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	owner_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'), nullable=False)
	hungry: Mapped[int] = mapped_column(nullable=False, default=65)
	mood: Mapped[int] = mapped_column(nullable=False, default=71)
	decrease_food_value: Mapped[int] = mapped_column(nullable=False, default=1)
	decrease_mood_value: Mapped[int] = mapped_column(nullable=False, default=0)
	state: Mapped[PupaState] = mapped_column(nullable=False, default=PupaState.nothing)
	poop_state: Mapped[bool] = mapped_column(nullable=False, default=False)
	self_education_stat: Mapped[Int64] = mapped_column(nullable=False, default=0)
	schedule_food_id: Mapped[str] = mapped_column(nullable=True)
	sleep_schedule_id: Mapped[str] = mapped_column(nullable=True)
	sleep_time: Mapped[str] = mapped_column(nullable=True)
	sleep_state: Mapped[bool] = mapped_column(nullable=False, server_default='false')