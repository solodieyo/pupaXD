import asyncpg
import asyncio

from asyncpg import Connection


async def main():
	conn: Connection = await asyncpg.connect(
		user="pugach",
		password="qweqwe",
		database="pupadb",
		host="localhost",
		port=5432
	)

	try:
		query = """
        UPDATE pupa
        SET iq = CASE
            WHEN iq > 2 THEN iq - 2
            ELSE 0
        END;
        """
		await conn.execute(query)
	finally:
		await conn.close()


asyncio.run(main())
