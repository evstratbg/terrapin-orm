from typing import Any
from .fields.base import Field, IndexedField, UnselectedField
from .sql import SQLManager
from .connection import _EXECUTORS


class Config:
    """Table configuration."""

    table_name: str = None
    db_alias: str = "default"
    abstract: bool = True


class BaseTableMeta(type):
    def __new__(cls, name, bases, attrs):
        columns = []
        for attr_name, attr_value in attrs.items():
            if isinstance(attr_value, Field):
                columns.append(attr_name)
        attrs["_columns"] = columns
        return super().__new__(cls, name, bases, attrs)


class Table(metaclass=BaseTableMeta):
    """Base class for database tables."""
    config = Config

    def __init__(self, **kwargs: Any) -> None:
        for column in self._columns:
            # print(column, kwargs.get(column))
            setattr(self, column, kwargs.get(column, UnselectedField))

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if attr is UnselectedField:
            raise AttributeError(f"Column '{name}' was\'t selected")
        return attr

    @property
    def table_name(self) -> str:
        table_name = self.__class__.__name__.lower()
        if self.config.table_name:
            table_name = self.config.table_name
        return table_name

    @classmethod
    def sql(cls):
        """Generate SQL statement to create the table."""
        fields = {k: v for k, v in cls.__dict__.items() if isinstance(v, Field)}
        table_name = cls.config.table_name

        field_definitions = []
        field_indexes = []
        for name, field in fields.items():
            field_definitions.append(f"{name} {field.sql()}")
            if isinstance(field, IndexedField) and field.index:
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
    async def drop(cls):
        """Create table in database."""
        sql = f"DROP TABLE {cls.config.table_name};"
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
    def update(cls, *kwargs: tuple[Field, Any]):
        return SQLManager(cls).update(*kwargs)

    @classmethod
    def insert(cls, **kwargs: dict[str, Any]):
        return SQLManager(cls).insert(**kwargs)
