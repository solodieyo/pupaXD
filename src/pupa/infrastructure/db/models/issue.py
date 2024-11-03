from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from pupa.infrastructure.db.models import Base


class Issue(Base):
	__tablename__ = "issues"

	id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
	issue_text: Mapped[Optional[str]]
	from_user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
