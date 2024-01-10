from ..connection import _EXECUTORS
from ..table import _T
from .base import BaseSQLManager


class DropTableSQLManager(BaseSQLManager[_T]):
    def _prepare_sql(self):
        return f"DROP TABLE IF EXISTS {self.table_name}"

    async def coro(self) -> str:
        sql_string = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        response = await executor.execute(sql_string)
        return response.split(" ")[-1]
