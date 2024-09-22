from sqlalchemy import select

from pupa.infrastructure.db.models.pupa import Pupa
from pupa.infrastructure.db.repositories import BaseRepository


class PupaRepository(BaseRepository):
	async def create_user_pupa(
		self,
		owner_id: int,
	):
		pupa = Pupa(owner_id=owner_id)

		self.session.add(pupa)
		await self.session.commit()

	async def get_pupa_state(
		self,
		owner_id: int,
	):
		pupa = await self.session.scalars(
			select(Pupa).where(Pupa.owner_id == owner_id)
		)

		return pupa