from itertools import chain
from typing import Any, Sequence

from .connection import _EXECUTORS
from .fields.base import Field
from .fields.operations import Operator
from .table import Table


class SQLManager:
    def __init__(self, table: type[Table] | None = None):
        self.parts = {}
        self._vars_counter = 0
        self.table = table
        self.table_name = table.table_name() if table else None

    def set_table(self, table: Table):
        self.table = table
        self.table_name = table.table_name()
        return self

    def from_(self, table: Table):
        self.set_table(table)
        return self

    def select(self, *columns: Field):
        """
        Generate SQL SELECT statement for the table.

        :param columns: List of columns to select. Selects all if none provided.
        :return: Generated SQL SELECT statement as a string.
        """

        if not columns:
            columns = self.table._columns
        else:
            columns = [f.name for f in columns if isinstance(f, Field)]
        self.parts["select"] = {"columns": columns}
        return self

    def select_for_update(self, *columns: Field, nowait: bool, skip_locked: bool):
        if not columns:
            columns = self.table._columns
        else:
            columns = [f.name for f in columns if isinstance(f, Field)]
        self.parts["select_for_update"] = {
            "columns": columns,
            "nowait": nowait,
            "skip_locked": skip_locked,
        }
        return self

    def set(self, **kwargs: dict[str, Field | Operator]):
        self.parts["update"] = []
        for left, right in kwargs.items():
            op = "="
            if isinstance(right, Operator):
                left = f"{left}={right.column}"
                op = right.op
                right = right.value
            self.parts["update"].append({"left": left, "op": op, "right": right})
        return self

    def values(self, **kwargs: dict[str, Any]):
        self.parts["insert"] = {"columns": list(kwargs.keys()), "values": list(kwargs.values())}
        return self

    def delete(self):
        self.parts["delete"] = True
        return self

    def returning(self, *columns: Field):
        if not columns:
            columns = self.table._columns
        else:
            columns = [f.name for f in columns if isinstance(f, Field)]
        self.parts["returning"] = {"columns": columns}
        return self

    def order_by(self, *columns: Field):
        self.parts["order_by"] = {"columns": columns}
        return self

    def limit(self, limit: int):
        self.parts["limit"] = limit
        return self

    def offset(self, offset: int):
        self.parts["offset"] = offset
        return self

    def where(self, *args: Sequence[Operator], **kwargs: dict[str, Operator | Any]):
        self.parts.setdefault("where", [])
        for arg in args:
            arg: Operator
            left, op, right = arg.resolve()
            self.parts.setdefault("where", []).append({"right": right, "op": op, "left": left})
        for left, right in kwargs.items():
            op = "="
            if isinstance(right, Operator):
                left = f"{left}={right.column}"
                op = right.op
                right = right.value
            self.parts.setdefault("where", []).append({"right": right, "op": op, "left": left})
        return self

    def _resolve_quotes(self, value: Any):
        self._vars_counter += 1
        if isinstance(value, (int, float, bool, str)):
            return f"${self._vars_counter}"
        if isinstance(value, (list, tuple)):
            values = []
            for v in value:
                values.append(self._resolve_quotes(v))
            return f"({', '.join(values)})"
        else:
            return value

    def _prepate_sql(self):
        self._vars_counter = 0
        sql_string = ""
        query_args = []
        if self.parts.get("select"):
            columns = self.parts["select"]["columns"]
            sql_string += f"SELECT {', '.join(columns)} FROM {self.table_name}"

        elif self.parts.get("select_for_update"):
            columns = self.parts["select_for_update"]["columns"]
            sql_string += f"SELECT FOR UPDATE {', '.join(columns)} FROM {self.table_name}"

        elif self.parts.get("update"):
            values_sql = []
            for part in self.parts["update"]:
                right = part["right"]
                op = part["op"]
                left = part["left"]

                prepared_value = self._resolve_quotes(right)
                values_sql.append(f"{left}{op}{prepared_value}")
                query_args.append(right)
            sql_string += f"UPDATE {self.table_name} SET {','.join(values_sql)}"

        elif self.parts.get("delete"):
            sql_string += f"DELETE FROM {self.table_name}"

        elif self.parts.get("returning"):
            columns = self.parts["returning"]["columns"]
            sql_string += f" RETURNING {', '.join(columns)}"

        elif self.parts.get("insert"):
            columns = self.parts["insert"]["columns"]
            values = self.parts["insert"]["values"]
            values_sql = []
            for value in values:
                values_sql.append(self._resolve_quotes(value))

            sql_string += f"INSERT INTO {self.table_name} ({', '.join(columns)}) VALUES ({', '.join(values_sql)})"
            query_args = values

        where_clause = " WHERE "
        clauses = []
        for part in self.parts.get("where", []):
            left = part["left"]
            op = part["op"]
            right = part["right"]

            prepared_value = self._resolve_quotes(right)
            if op == "colum_modifier":
                clauses.append(f"{left}{prepared_value}")
            else:
                clauses.append(f"{left}{op}{prepared_value}")

            query_args.append(right)

        if clauses:
            sql_string += where_clause
            sql_string += " AND ".join(clauses)

        if self.parts.get("select_for_update"):
            if self.parts["select_for_update"]["nowait"]:
                sql_string += " NOWAIT"
            elif self.parts["select_for_update"]["skip_locked"]:
                sql_string += " SKIP LOCKED"

        return sql_string, list(chain(query_args))

    async def coro(self):
        sql_string, query_args = self._prepate_sql()
        if self.parts.get("select") or self.parts.get("select_for_update"):
            records = await _EXECUTORS["postgres"].fetchall(sql_string, *query_args)
            if records:
                return [self.table(**r) for r in records]
            return None
        response = await _EXECUTORS["postgres"].execute(sql_string, *query_args)
        return response.split(" ")[-1]

    def __await__(self):
        return self.coro().__await__()
