from sqlalchemy import ForeignKey, INTEGER
from sqlalchemy.orm import Mapped, mapped_column

from pupa.bot.enums import PupaState
from pupa.infrastructure.db.models import Base, Int64, Int16


class Pupa(Base):
	__tablename__ = "pupa"
	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	owner_id: Mapped[Int64] = mapped_column(ForeignKey('users.id'), nullable=False)
	hungry: Mapped[int] = mapped_column(nullable=False, default=100)
	mood: Mapped[int] = mapped_column(nullable=False, default=100)
	decrease_food_value: Mapped[int] = mapped_column(nullable=False, default=2)
	decrease_mood_value: Mapped[int] = mapped_column(nullable=False, default=2)
	state: Mapped[PupaState] = mapped_column(nullable=False, default=PupaState.nothing)
	poop_state: Mapped[bool] = mapped_column(nullable=False, default=False)
	self_education_stat: Mapped[Int64] = mapped_column(nullable=False, default=0)