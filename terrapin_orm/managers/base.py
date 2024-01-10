from abc import abstractmethod
from collections.abc import Generator, Sequence
from typing import Any, Generic

from ..fields.operations import Operator
from ..table import _T


class BaseSQLManager(Generic[_T]):
    def __init__(self, table: type[_T] | None = None):
        self._vars_counter = 0
        self.table = table

    @property
    def table_name(self):
        return self.table.config.table_name if self.table else None

    def _resolve_quotes(self, value: Any):
        self._vars_counter += 1
        if isinstance(value, int | float | bool | str):
            return f"${self._vars_counter}"
        if isinstance(value, list | tuple):
            values = []
            for v in value:
                values.append(self._resolve_quotes(v))
            return f"({', '.join(values)})"
        else:
            return value

    @abstractmethod
    def _prepare_sql(self):
        raise NotImplementedError

    @abstractmethod
    async def coro(self) -> list[_T] | None:
        raise NotImplementedError

    def __await__(self) -> Generator[Any, None, list[_T]]:
        return self.coro().__await__()


class BaseSQLManagerFiltering(BaseSQLManager[_T]):
    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)
        self.where_conditions = []

    def where(self, *args: Sequence[Operator], **kwargs: dict[str, Operator | Any]):
        for arg in args:
            arg: Operator
            left, op, right = arg.resolve()
            self.where_conditions.append({"right": right, "op": op, "left": left})

        for left, right in kwargs.items():
            op = "="
            if isinstance(right, Operator):
                left = f"{left}={right.column}"  # noqa: PLW2901
                op = right.op
                right = right.value  # noqa: PLW2901
            self.where_conditions.append({"right": right, "op": op, "left": left})
        return self

    def _prepare_where_sql(self):
        query_args = []
        sql_string = ""
        if self.where_conditions:
            where_clause = " WHERE "
            clauses = []
            for part in self.where_conditions:
                left = part["left"]
                op = part["op"]
                right = part["right"]

                prepared_value = self._resolve_quotes(right)
                if op == "colum_modifier":
                    clauses.append(f"{left}{prepared_value}")
                else:
                    clauses.append(f"{left}{op}{prepared_value}")

                query_args.append(right)

            sql_string += where_clause
            sql_string += " AND ".join(clauses)
        return sql_string, list(query_args)

    @abstractmethod
    def _prepare_sql(self):
        raise NotImplementedError

    @abstractmethod
    async def coro(self) -> list[_T] | None | int:
        raise NotImplementedError
