from dataclasses import dataclass

from sqlalchemy import URL


LOCALES_PATH = ''
CONFIG_PATH = r"config.toml"


@dataclass
class Tg:
	token: str
	admins_id: list[int]
	idea_channel_id: str


@dataclass
class Postgres:
	database: str
	user: str
	password: str
	host: str
	port: int

	def build_dsn(self) -> URL:
		return URL.create(
			drivername="postgresql+asyncpg",
			username=self.user,
			password=self.password,
			host=self.host,
			port=self.port,
			database=self.database,
		)


@dataclass
class Redis:
	host: str
	port: int


@dataclass
class AppConfig:
	tg: Tg
	postgres: Postgres
	redis: Redis