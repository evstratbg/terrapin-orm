from typing import Any

from itertools import chain

from .fields.base import Field
from .connection import _EXECUTORS


class SQLManager:
    def __init__(self, table):
        self.table = table
        self.parts = {}
        self._vars_counter = 0

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
        self.parts["select_for_update"] = {"columns": columns, "nowait": nowait, "skip_locked": skip_locked}
        return self

    def update(self, *args: Field):
        self.parts["update"] = [dict(a) for a in args]
        return self

    def insert(self, **kwargs: dict[str, Any]):
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

    def where(self, *args: tuple[Field, Any]):
        self.parts.setdefault("where", []).extend(dict(a) for a in args)
        return self

    def _resolve_quotes(self, value: Any):
        self._vars_counter += 1
        if isinstance(value, (int, float, bool, str)):
            return f"${self._vars_counter}"
        elif isinstance(value, (list, tuple)):
            values = []
            for v in value:
                values.append(self._resolve_quotes(v))
            return f"({', '.join(values)})"
        else:
            return value

    def _prepate_sql(self):
        sql_string = ""
        query_args = []
        if self.parts.get("select"):
            columns = self.parts['select']['columns']
            sql_string += f"SELECT {', '.join(columns)} FROM {self.table.config.table_name}"

        elif self.parts.get("select_for_update"):
            columns = self.parts['select_for_update']['columns']
            sql_string += f"SELECT FOR UPDATE{', '.join(columns)} FROM {self.table.config.table_name}"

        elif self.parts.get("update"):
            values_sql = []
            for part in self.parts['update']:
                value = part["value"]
                op = part["op"]
                column = part["column"]

                prepared_value = self._resolve_quotes(value)
                if op == "=":
                    values_sql.append(f"{column}={prepared_value}")
                else:
                    values_sql.append(f"{column}={column}{op}{prepared_value}")
                query_args.append(value)
            sql_string += f"UPDATE {self.table.config.table_name} SET {','.join(values_sql)}"

        elif self.parts.get("delete"):
            sql_string += f"DELETE FROM {self.table.config.table_name}"

        elif self.parts.get("returning"):
            columns = self.parts['returning']['columns']
            sql_string += f" RETURNING {', '.join(columns)}"
        elif self.parts.get("insert"):
            columns = self.parts["insert"]["columns"]
            values = self.parts["insert"]["values"]
            values_sql = []
            for value in values:
                values_sql.append(self._resolve_quotes(value))
            sql_string += f"INSERT INTO {self.table.config.table_name} ({', '.join(columns)}) VALUES ({', '.join(values_sql)}) RETURNING {', '.join(self.table._columns)}"
            query_args = values

        where_clause = " WHERE "
        clauses = []
        for part in self.parts.get("where", []):
            value = part["value"]
            op = part["op"]
            column = part["column"]

            clause = f'"{column}" {op} ' + self._resolve_quotes(value=value)
            query_args.append(value)
            clauses.append(clause)

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
        print(sql_string, query_args)
        if self.parts.get("select") or self.parts.get("select_for_update"):
            records = await _EXECUTORS["postgres"].fetchall(sql_string, *query_args)
            if records:
                return [self.table(**r) for r in records]
        else:
            response = await _EXECUTORS["postgres"].execute(sql_string, *query_args)
            return response.split(" ")[-1]

    def __await__(self):
        return self.coro().__await__()


class Meta:
    def __init__(self, table):
        self.sql_manager = SQLManager(table)
