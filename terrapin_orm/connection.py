from typing import Any

import asyncpg


class Executor:
    def __init__(
            self,
            pool: asyncpg.pool.Pool,
            password: str,
            host: str,
            port: int,
            database: str,
    ):
        self._pool = pool
        self.password = password
        self.host = host
        self.port = port
        self.database = database

    async def execute(self, query: str, *args: Any, timeout: float | None = None) -> str:
        """Execute an SQL command (or commands).

        This method can execute many SQL commands at once, when no arguments
        are provided.
        """
        async with self._pool.acquire() as conn:
            return await conn.execute(query, *args, timeout=timeout)

    async def executemany(self, command: str, args: Any, *, timeout: int | None = None):
        """Execute an SQL *command* for each sequence of arguments in *args*."""
        async with self._pool.acquire() as conn:
            return await conn.executemany(command, *args, timeout=timeout)

    async def fetchval(self, query: str, *args: Any, column: int = 0, timeout: int | None = None):
        """Run a query and return a value in the first row.

        :param str query: Query text.
        :param args: Query arguments.
        :param int column: Numeric index within the record of the value to
                           return (defaults to 0).
        :param float timeout: Optional timeout value in seconds.
                            If not specified, defaults to the value of
                            ``command_timeout`` argument to the ``Connection``
                            instance constructor.

        :return: The value of the specified column of the first record, or
                 None if no records were returned by the query.
        """
        async with self._pool.acquire() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)

    async def fetchrow(
            self,
            query: str,
            *args: Any,
            timeout: int | None = None,
    ):
        """Run a query and return the first row."""

        async with self._pool.acquire() as conn:
            return await conn.fetchrow(query, *args, timeout=timeout)

    async def fetchall(
            self,
            query: str,
            *args: Any,
            timeout: int | None = None,
    ):
        """Run a query and return the first row."""

        async with self._pool.acquire() as conn:
            return await conn.fetch(query, *args, timeout=timeout)


_EXECUTORS: dict[str, Executor] = {}


class PoolManager:
    @classmethod
    async def add_pool(
            cls,
            username: str,
            password: str,
            host: str,
            port: int,
            database: str,
    ):
        dsn = cls.create_dsn(
            username=username,
            password=password,
            port=port,
            database=database,
            hostname=host,
        )
        pool = await asyncpg.create_pool(dsn)
        _EXECUTORS[database] = Executor(
            pool=pool,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    @staticmethod
    def create_dsn(
            username: str,
            password: str,
            hostname: str,
            port: int,
            database: str,
            scheme: str = "postgresql",
    ):
        return f"{scheme}://{username}:{password}@{hostname}:{port}/{database}"
