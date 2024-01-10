from typing import Any

from ..connection import _EXECUTORS
from ..fields.base import Field
from ..fields.operations import Operator
from ..table import _T
from .base import BaseSQLManagerFiltering


class UpdateSQLManager(BaseSQLManagerFiltering[_T]):
    def __init__(self, *args: Any, **kwargs: Any):
        self.returning_columns = kwargs.pop("returning_columns", None)
        self.update_clauses = kwargs.pop("update_clauses", [])
        super().__init__(*args, **kwargs)

    def returning(self, *columns: Field):
        if not columns:
            columns = self.table._columns
        else:
            columns = [f.name for f in columns if isinstance(f, Field)]
        return ReturningUpdateSQLManager(
            table=self.table,
            update_clauses=self.update_clauses,
            returning_columns=columns,
        )

    def set(self, *args: tuple[Operator], **kwargs: [int, str, list, tuple, dict, Operator, Field]):
        for left, right in kwargs.items():
            op = "="
            if isinstance(right, Operator):
                left = f"{left}={right.column}"  # noqa: PLW2901
                op = right.op
                right = right.value  # noqa: PLW2901
            self.update_clauses.append({"left": left, "op": op, "right": right})
        for arg in args:
            arg: Operator
            left, op, right = arg.resolve()
            self.update_clauses.append({"left": left, "op": op, "right": right})
        return self

    def _prepare_sql(self):
        values_sql = []
        query_args = []
        for part in self.update_clauses:
            right = part["right"]
            op = part["op"]
            left = part["left"]

            prepared_value = self._resolve_quotes(right)
            values_sql.append(f"{left}{op}{prepared_value}")
            query_args.append(right)
        sql_string = f"UPDATE {self.table_name} SET {','.join(values_sql)}"

        where_sql_string, where_query_args = self._prepare_where_sql()
        sql_string += where_sql_string
        query_args.extend(where_query_args)
        if self.returning_columns:
            sql_string += f" RETURNING {', '.join(self.returning_columns)}"
        return sql_string, list(query_args)

    async def coro(self) -> int:
        sql_string, query_args = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        records = await executor.execute(sql_string, *query_args)
        return int(records.split(" ")[-1])


class ReturningUpdateSQLManager(UpdateSQLManager[_T]):
    async def coro(self):
        sql_string, query_args = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        records = await executor.fetchall(sql_string, *query_args)
        return [self.table(**r) for r in records]
