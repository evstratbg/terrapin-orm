from typing import Any

from ..connection import _EXECUTORS
from ..fields.operations import Operator
from ..table import _T
from .base import BaseSQLManager


class InsertSQLManager(BaseSQLManager[_T]):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.values_to_insert = []

    def values(self, *rows: list[Operator] | list[list[Operator]]):
        if not isinstance(rows[0], list):
            rows = [rows]
        for row in rows:
            data_to_insert = {}
            for arg in row:
                arg: Operator
                left, op, right = arg.resolve()
                data_to_insert.update({left: right})
            self.values_to_insert.append(data_to_insert)
        return self

    def _prepare_sql(self):
        values = []
        values_sql = []
        columns = set()
        for row in self.values_to_insert:
            values_sql_to_insert = []
            for column, value in row.items():
                columns.add(column)
                values.append(value)
                values_sql_to_insert.append(self._resolve_quotes(value))
            values_sql.append(f"({', '.join(values_sql_to_insert)})")

        sql_string = f"INSERT INTO {self.table_name} ({', '.join(columns)})"
        sql_string += f" VALUES {', '.join(values_sql)} RETURNING *"
        return sql_string, values

    async def coro(self):
        sql_string, query_args = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        records = await executor.fetchall(sql_string, *query_args)
        return [self.table(**r) for r in records]
