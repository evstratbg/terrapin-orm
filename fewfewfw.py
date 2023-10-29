import asyncpg


async def main():
    async with asyncpg.create_pool(
        dsn="postgresql://postgres:postgres@localhost:5432/postgres"
    ) as pool:
        await pool.execute("INSERT INTO users (id, age) VALUES ($1, $2)", *[1, 10])


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())