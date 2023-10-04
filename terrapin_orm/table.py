from typing import Any

from .configs import TableConfig
from .connection import _EXECUTORS
from .fields.base import Field, IndexedField, PkField, UnselectedField
from .sql import SQLManager


class BaseTableMeta(type):
    def __new__(cls, name: str, bases: tuple, attrs: dict) -> object:
        columns = []
        pk = None
        if "config" not in attrs:
            raise ValueError(f"Table {name} must have `config` attribute")
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                columns.append(attr_name)
            if isinstance(attr_value, PkField) and attr_value.pk:
                pk = attr_name

        attrs["_columns"] = columns
        attrs["_pk"] = pk
        return super().__new__(cls, name, bases, attrs)


class Table(metaclass=BaseTableMeta):
    """Base class for database tables."""
    config = TableConfig(table_name="", db_alias="default", abstract=True)

    def __init__(self, **kwargs: [str, [str, int, bool, dict, list, tuple]]) -> None:
        self.raw_data = kwargs
        for column in self._columns:
            setattr(self, column, kwargs.get(column, UnselectedField))

    def __getattribute__(self, name: str):
        attr = super().__getattribute__(name)
        if attr is UnselectedField:
            raise AttributeError(f"Column '{name}' was\'t selected")
        return attr

    @classmethod
    def table_name(cls) -> str:
        return cls.config.table_name

    @classmethod
    def sql(cls):
        """Generate SQL statement to create the table."""
        fields = {k: v for k, v in cls.__dict__.items() if isinstance(v, Field)}
        table_name = cls.table_name()

        field_definitions = []
        field_indexes = []
        for name, field in fields.items():
            field_definitions.append(f"{name} {field.sql()}")
            if isinstance(field, IndexedField) and field.index:
                field_indexes.append(
                    field.index_sql(table_name, name),
                )
            if isinstance(field, PkField) and field.pk:
                field_indexes.append(
                    field.index_sql(table_name, name),
                )

        field_definitions_sql = "\n\t"
        field_definitions_sql += ",\n\t".join(field_definitions)
        field_definitions_sql += "\n"
        field_indexes = "\n".join(field_indexes)

        return f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions_sql});\n{field_indexes}"

    @classmethod
    async def create_table(cls):
        """Create table in database."""
        sql = cls.sql()
        return await _EXECUTORS["postgres"].execute(sql)

    @classmethod
    async def drop_table(cls):
        """Create table in database."""
        sql = f"DROP TABLE {cls.table_name()};"
        return await _EXECUTORS["postgres"].execute(sql)

    @classmethod
    def select_for_update(cls, *fields: Field, nowait: bool = False, skip_locked: bool = False):
        return SQLManager(cls).select_for_update(*fields, nowait=nowait, skip_locked=skip_locked)

    @classmethod
    def select(cls, *fields: Field):
        return SQLManager(cls).select(*fields)

    @classmethod
    def where(cls, *fields: tuple[Field, Any]):
        return SQLManager(cls).where(*fields)

    @classmethod
    def delete(cls):
        return SQLManager(cls).delete()

    @classmethod
    def update(cls):
        return SQLManager(cls)

    @classmethod
    def set(cls, *kwargs: tuple[Field, Any]):
        return SQLManager(cls).set(*kwargs)

    @classmethod
    def insert(cls, **kwargs: dict[str, str | int | bool | dict | list | tuple]):
        if not kwargs:
            raise ValueError("Nothing to insert")
        unknown_columns = set(kwargs) - set(cls._columns)
        if unknown_columns:
            raise ValueError("Unknown columns: " + ", ".join(unknown_columns))
        return SQLManager(cls).insert(**kwargs)
