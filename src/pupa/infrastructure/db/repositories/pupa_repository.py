from sqlalchemy import select

from pupa.infrastructure.db.models.pupa import Pupa
from pupa.infrastructure.db.repositories import BaseRepository


class PupaRepository(BaseRepository):
	async def get_or_create_pupa(
		self,
		owner_id: int,
	) -> Pupa:
		pupa = await self.session.scalar(
			select(Pupa).where(Pupa.owner_id == owner_id)
		)

		if pupa is None:
			pupa = Pupa(owner_id=owner_id)
			self.session.add(pupa)
			await self.session.commit()
		return pupa
