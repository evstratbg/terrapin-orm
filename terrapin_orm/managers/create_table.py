from ..connection import _EXECUTORS
from ..fields.base import Field, IndexedField, PkField
from ..table import _T
from .base import BaseSQLManager


class CreateTableSQLManager(BaseSQLManager[_T]):
    def _prepare_sql(self):
        fields = {k: v for k, v in self.table.__dict__.items() if isinstance(v, Field)}

        field_definitions = []
        field_indexes = []
        for name, field in fields.items():
            field_definitions.append(f"{name} {field.sql()}")
            if isinstance(field, IndexedField) and field.index:
                field_indexes.append(
                    field.index_sql(self.table_name, name),
                )
            if isinstance(field, PkField) and field.pk:
                field_indexes.append(
                    field.index_sql(self.table_name, name),
                )

        field_definitions_sql = "\n\t"
        field_definitions_sql += ",\n\t".join(field_definitions)
        field_definitions_sql += "\n"
        field_indexes = "\n".join(field_indexes)

        return f"CREATE TABLE IF NOT EXISTS {self.table_name} ({field_definitions_sql});\n{field_indexes}"

    async def coro(self) -> str:
        sql_string = self._prepare_sql()
        executor = _EXECUTORS[self.table.config.db_alias]
        response = await executor.execute(sql_string)
        return response.split(" ")[-1]
