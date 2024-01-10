from ..connection import _EXECUTORS
from ..table import _T
from .base import BaseSQLManagerFiltering


class DeleteSQLManager(BaseSQLManagerFiltering[_T]):
    def _prepare_sql(self):
        sql_string = f"DELETE FROM {self.table_name}"
        where_sql_string, query_args = self._prepare_where_sql()
        sql_string += where_sql_string
        return sql_string, list(query_args)

    async def coro(self):
        sql_string, query_args = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        response = await executor.execute(sql_string, *query_args)
        return response.split(" ")[-1]
