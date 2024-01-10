from typing import Any

from ..connection import _EXECUTORS
from ..fields.base import Field
from ..table import _T
from .base import BaseSQLManagerFiltering


class SelectSQLManager(BaseSQLManagerFiltering[_T]):
    def __init__(self, select_for_update: bool, skip_locked: bool, nowait: bool, *args: Any, **kwargs: Any):
        columns = kwargs.pop("columns", None)
        super().__init__(*args, **kwargs)
        self._order_by = []
        self._limit = None
        self._offset = None

        self.column_names = [c.name for c in columns] or ["*"]
        self.select_for_update = select_for_update
        self.nowait = nowait
        self.skip_locked = skip_locked
        if self.select_for_update and self.skip_locked:
            raise ValueError("Cannot use both `nowait` and `skip_locked` at the same time.")

    def from_(self, table: type[_T]):
        self.table = table
        return self

    def _prepare_sql(self):
        sql_string = "SELECT "
        sql_string += f"{', '.join(self.column_names)} FROM {self.table_name}"
        where_sql_string, query_args = self._prepare_where_sql()
        sql_string += where_sql_string

        # order matters
        if self._order_by:
            sql_string += f" ORDER BY {', '.join(self._order_by)}"
        if self._limit:
            sql_string += f" LIMIT {self._limit}"
        if self._offset:
            sql_string += f" OFFSET {self._offset}"

        if self.select_for_update:
            sql_string += " FOR UPDATE "
            sql_string = sql_string.strip()
        if self.nowait:
            sql_string += " NOWAIT"
        if self.skip_locked:
            sql_string += " SKIP LOCKED"
        return sql_string, list(query_args)

    def order_by(self, *columns: Field):
        self._order_by = [c.name for c in columns]
        return self

    def limit(self, limit: int):
        self._limit = limit
        return self

    def offset(self, offset: int):
        self._offset = offset
        return self

    async def coro(self):
        sql_string, query_args = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        records = await executor.fetchall(sql_string, *query_args)
        return [self.table(**r) for r in records]
