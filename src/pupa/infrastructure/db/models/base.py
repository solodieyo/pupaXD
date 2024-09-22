from typing import Annotated, TypeAlias
from datetime import datetime, timezone

from sqlalchemy import Integer, BigInteger, DateTime, func
from sqlalchemy.orm import DeclarativeBase, registry, Mapped, mapped_column

Int16: TypeAlias = Annotated[int, 16]
Int64: TypeAlias = Annotated[int, 64]


class Base(DeclarativeBase):
	registry = registry(
		type_annotation_map={Int16: Integer, Int64: BigInteger, datetime: DateTime(timezone=True)}
	)
	created_at: Mapped[datetime] = mapped_column(server_default=func.now())
	updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
