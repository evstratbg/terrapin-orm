from abc import abstractmethod
from collections.abc import Iterable as It
from typing import Any

from .operations import Add, Contains, Div, Eq, Gt, Gte, IAdd, IDiv, IMul, ISub, Lt, Lte, Mul, NotEq, Sub


class UnselectedField:
    pass


class Field:
    """Generic field without specific constraints."""
    def __init__(self):
        self.name = None
        self.value = None

    @abstractmethod
    def sql(self):
        raise NotImplementedError("Subclasses must implement the sql method")

    def in_(self, value: It):
        return Contains(self.name, value)

    def __set_name__(self, owner: Any, name: str):
        self.name = name

    def __set__(self, instance: Any, value: Any):
        self.value = value

    def __eq__(self, other: object):
        return Eq(self.name, other)

    def __ne__(self, other: object):
        return NotEq(self.name, other)

    def __gt__(self, other: Any):
        return Gt(self.name, other)

    def __ge__(self, other: Any):
        return Gte(self.name, other)

    def __lt__(self, other: Any):
        return Lt(self.name, other)

    def __le__(self, other: Any):
        return Lte(self.name, other)

    def __sub__(self, other: Any):
        return Sub(self.name, other)

    def __add__(self, other: Any):
        return Add(self.name, other)

    def __iadd__(self, other: Any):
        return IAdd(self.name, other)

    def __isub__(self, other: Any):
        return ISub(self.name, other)

    def __mul__(self, other: Any):
        return Mul(self.name, other)

    def __imul__(self, other: Any):
        return IMul(self.name, other)

    def __truediv__(self, other: Any):
        return Div(self.name, other)

    def __itruediv__(self, other: Any):
        return IDiv(self.name, other)

    @abstractmethod
    def python_type(self):
        raise NotImplementedError("Subclasses must implement the `python_type` method")


class IndexedField(Field):
    """A base field class that supports indexing."""

    def __init__(self, index: bool = False):
        super().__init__()
        self.index = index

    def index_sql(self, table_name: str, column_name: str):
        if self.index:
            return f"CREATE INDEX idx_{table_name}_{column_name} ON {table_name} ({column_name});"
        return ""


class PkField(Field):
    """A base field class that supports indexing."""

    def __init__(self, index: bool = False, pk: bool = False):
        super().__init__()
        self.index = index
        self.pk = pk

    def index_sql(self, table_name: str, column_name: str):
        if self.index:
            return f"CREATE INDEX idx_{table_name}_{column_name} ON {table_name} ({column_name});"
        return ""


class ArrayField(IndexedField):
    """Base array field. Can contain multiple items of a specified data type."""

    def __init__(self, item_type: str):
        super().__init__()
        self.item_type = item_type

    def sql(self):
        return f"{self.item_type}[]"

    def python_type(self):
        return list
