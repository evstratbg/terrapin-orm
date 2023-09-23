from .base import BaseField, BaseIndexedField


class VarcharField(BaseIndexedField):
    """Variable-length character string. Can contain up to N characters."""

    def __init__(self, max_length: int | None = None, index: bool = False):
        super().__init__()
        self.max_length = max_length
        self.index = index

    def sql(self):
        """Generate SQL for the VARCHAR field definition."""
        return f"VARCHAR({self.max_length})" if self.max_length else "VARCHAR"

    def index_sql(self, table_name: str, column_name: str):
        """Generate SQL for the index of the VARCHAR field if indexing is set."""
        if self.index:
            # Assuming there's a way to reference table_name and column_name
            # from within the field to create an index name. Adjust if needed.
            return f"CREATE INDEX idx_{table_name}_{column_name} ON {table_name} ({column_name});"
        return ""


class TextField(BaseField):
    """Unlimited length text field."""

    def sql(self):
        return "TEXT"
