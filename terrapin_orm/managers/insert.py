from typing import Any

from ..connection import _EXECUTORS
from ..fields.operations import Operator
from ..table import _T
from .base import BaseSQLManager


class InsertSQLManager(BaseSQLManager[_T]):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.values_to_insert = {}

    def values(self, *args: tuple[Operator], **kwargs: [int, str, list, tuple, dict]):
        self.values_to_insert.update(**kwargs)
        for arg in args:
            arg: Operator
            left, op, right = arg.resolve()
            self.values_to_insert.update({left: right})
        return self

    def _prepare_sql(self):
        values = []
        values_sql = []
        columns = []
        for column, value in self.values_to_insert.items():
            columns.append(column)
            values.append(value)
            values_sql.append(self._resolve_quotes(value))

        sql_string = f"INSERT INTO {self.table_name} ({', '.join(columns)})"
        sql_string += f" VALUES ({', '.join(values_sql)}) RETURNING *"
        return sql_string, values

    async def coro(self):
        sql_string, query_args = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        records = await executor.fetchall(sql_string, *query_args)
        return [self.table(**r) for r in records]
