from sqlalchemy import update, select

from pupa.infrastructure.db.models.theme import Theme
from pupa.infrastructure.db.repositories import BaseRepository


class ThemeRepository(BaseRepository):

	async def create_theme(
		self,
		theme_name: str,
	):
		theme = Theme(theme_name=theme_name)
		self.session.add(theme)
		await self.session.commit()

	async def delete_theme(
		self,
		theme_id: int,
	):
		await self.session.execute(
			update(Theme).where(Theme.id == theme_id).values(
				deleted=True
			)
		)
		await self.session.commit()

	async def change_theme_tittle(
		self,
		theme_id: int,
		theme_name: str,
	):
		await self.session.execute(
			update(Theme).where(Theme.id == theme_id).values(
				theme_name=theme_name
			)
		)
		await self.session.commit()

	async def get_themes(self):
		themes = await self.session.execute(
			select(Theme).where(Theme.deleted == False)
		)
		return themes.scalars().all()