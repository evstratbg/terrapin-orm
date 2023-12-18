
from .configs import TableConfig
from .fields.base import Field, PkField, UnselectedField


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

