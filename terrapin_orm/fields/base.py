from abc import abstractmethod


class BaseField:
    """Generic field without specific constraints."""

    @abstractmethod
    def sql(self):
        raise NotImplementedError("Subclasses must implement the sql method")


class BaseIndexedField(BaseField):
    """A base field class that supports indexing."""

    def __init__(self, index: bool = False):
        super().__init__()
        self.index = index

    def index_sql(self, table_name: str, column_name: str):
        if self.index:
            return f"CREATE INDEX idx_{table_name}_{column_name} ON {table_name} ({column_name});"
        return ""


class BaseArrayField(BaseField):
    """Base array field. Can contain multiple items of a specified data type."""

    def __init__(self, item_type: str):
        self.item_type = item_type

    def sql(self):
        return f"{self.item_type}[]"
