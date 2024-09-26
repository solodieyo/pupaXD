
from sqlalchemy import select, update

from pupa.bot.enums import PupaState
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

	async def get_pupa_state(
		self,
		owner_id: int,
	):
		pupa = await self.session.scalar(
			select(Pupa).where(Pupa.owner_id == owner_id)
		)

		return pupa

	async def get_pupa_by_pupa_id(self, pupa_id: int):
		pupa = await self.session.scalar(
			select(Pupa).where(Pupa.id == pupa_id)
		)

		return pupa

	async def inscribe_education_time(self, pupa_id: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				self_education_stat=Pupa.self_education_stat + 0.1
			)
		)
		await self.session.commit()

	async def decrease_hungry(self, pupa_id: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				hungry=Pupa.hungry - Pupa.decrease_food_value
			)
		)
		await self.session.commit()

	async def decrease_mood(self, pupa_id: int):
		poop_state = await self.session.execute(
			select(Pupa.poop_state).where(Pupa.id == pupa_id)
		)
		minus_mood = 5 if poop_state.fetchone() else 0

		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				mood=Pupa.mood - (Pupa.decrease_mood_value + minus_mood)
			)
		)
		await self.session.commit()

	async def decrease_food(self, pupa_id: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				food=Pupa.hungry - Pupa.decrease_food_value
			)
		)
		await self.session.commit()

	async def set_poop_state(self, pupa_id: int, status: bool):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				poop_state=status
			)
		)
		await self.session.commit()

	async def set_state(self, pupa_id: int, state: PupaState):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				state=state
			)
		)
		await self.session.commit()

	async def set_decrease_values(
		self,
		pupa_id: int,
		mood: int,
		hungry: int
	):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				decrease_mood_value=mood,
				decrease_food_value=hungry
			)
		)
		await self.session.commit()

	async def inscribe_mood(self, pupa_id: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				mood=Pupa.mood + 1
			)
		)
		await self.session.commit()

	async def inscribe_hungry(self, pupa_id: int, value: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				hungry=Pupa.hungry + value
			)
		)
		await self.session.commit()