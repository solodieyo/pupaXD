from datetime import datetime

from anyio.abc import value
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

	async def decrease_hungry_(self, pupa_id: int):
		pupa: Pupa = await self.get_pupa_by_pupa_id(pupa_id=pupa_id)
		if (pupa.hungry - pupa.decrease_food_value) >= 0:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id).values(
					hungry=Pupa.hungry - Pupa.decrease_food_value
				)
			)
		else:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id)
				.values(hungry=0)
			)
		await self.session.commit()

	async def decrease_mood_value(self, pupa_id: int, mood: int):
		if (mood - 1) >= 0:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id).values(
					mood=Pupa.mood - 1
				)
			)
		else:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id)
				.values(mood=0)
			)
		await self.session.commit()

	async def decrease_mood_(self, pupa_id: int):
		pupa: Pupa = await self.get_pupa_by_pupa_id(pupa_id=pupa_id)
		minus_mood = 5 if pupa.poop_state else 0
		if (pupa.mood - (pupa.decrease_mood_value - minus_mood)) >= 0:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id).values(
					mood=Pupa.mood - (Pupa.decrease_mood_value + minus_mood)
				)
			)
		else:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id)
				.values(mood=0)
			)
		await self.session.commit()

	async def decrease_mood_game(self, pupa_id: int, value: int = 1):
		pupa: Pupa = await self.get_pupa_by_pupa_id(pupa_id=pupa_id)
		if (pupa.mood - value) >= 0:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id).values(
					mood=Pupa.mood - value)
			)
		else:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id)
				.values(mood=0)
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

	async def inscribe_mood(self, pupa_id: int, value: int = 1):
		pupa: Pupa = await self.get_pupa_by_pupa_id(pupa_id=pupa_id)
		if (pupa.mood + value) <= 100:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id).values(
					mood=Pupa.mood + value)
			)
		else:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id)
				.values(mood=100)
			)
		await self.session.commit()

	async def inscribe_hungry(self, pupa_id: int, value: int):
		pupa: Pupa = await self.get_pupa_by_pupa_id(pupa_id=pupa_id)
		if (pupa.hungry + value) <= 100:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id).values(
					hungry=Pupa.hungry + value)
			)
		else:
			await self.session.execute(
				update(Pupa).where(Pupa.id == pupa_id)
				.values(hungry=100)
			)
		await self.session.commit()

	async def set_schedule_food_id(self, pupa_id: int, schedule_id: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				schedule_food_id=schedule_id
			)
		)
		await self.session.commit()

	async def delete_schedule_food_id(self, pupa_id: int):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				schedule_food_id=None
			)
		)
		await self.session.commit()

	async def set_sleep_time(self, pupa_id: int, time: str):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				sleep_time=time
			)
		)
		await self.session.commit()

	async def set_sleep_state(self, pupa_id: int, status: bool):
		await self.session.execute(
			update(Pupa).where(Pupa.id == pupa_id).values(
				sleep_state=status
			)
		)
		await self.session.commit()
