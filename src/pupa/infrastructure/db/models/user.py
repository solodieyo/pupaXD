from sqlalchemy.orm import Mapped, mapped_column

from pupa.infrastructure.db.models import Base, Int64, Int16


class User(Base):
	__tablename__ = 'users'

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	tg_user_id: Mapped[Int64]
	username: Mapped[str]
	full_name: Mapped[str]

