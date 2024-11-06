from sqlalchemy import select

from pupa.infrastructure.db.models import User
from pupa.infrastructure.db.repositories.base import BaseRepository


class UserRepository(BaseRepository):
	async def get_or_create_user(
		self,
		tg_user_id: int,
		username: str,
		full_name: str,

	):
		user = await self.session.scalar(select(User).where(User.tg_user_id == tg_user_id))
		new_user = False

		if not user:
			user = User(
				tg_user_id=tg_user_id,
				username=username,
				full_name=full_name
			)
			self.session.add(user)
			new_user = True
			await self.session.commit()

		return user, new_user
