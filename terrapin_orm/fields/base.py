from abc import abstractmethod
from typing import Iterable as It, Any
from .operations import Eq, NotEq, Gt, Gte, Lt, Lte, Contains, Sub, Add


class UnselectedField:
    pass


class Field:
    """Generic field without specific constraints."""

    @abstractmethod
    def sql(self):
        raise NotImplementedError("Subclasses must implement the sql method")

    def in_(self, value: It):
        return Contains(self.name, value)

    def __set_name__(self, owner, name: str):
        self.name = name

    def __eq__(self, other: Any):
        return Eq(self.name, other)

    def __ne__(self, other: Any):
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
