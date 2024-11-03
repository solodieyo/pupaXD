from sqlalchemy.orm import mapped_column, Mapped

from pupa.infrastructure.db.models import Base, Int16


class Theme(Base):
	__tablename__ = "themes"

	id: Mapped[Int16] = mapped_column(primary_key=True, autoincrement=True)
	theme_name: Mapped[str] = mapped_column(nullable=False)
	deleted: Mapped[bool] = mapped_column(nullable=False, default=False)