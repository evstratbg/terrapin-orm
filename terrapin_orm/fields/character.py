from .base import Field, PkField


class VarcharField(PkField):
    """Variable-length character string. Can contain up to N characters."""

    def __init__(self, max_length: int | None = None, index: bool = False, pk: bool = False):
        super().__init__(index=index, pk=pk)
        self.max_length = max_length

    def sql(self):
        """Generate SQL for the VARCHAR field definition."""
        return f"VARCHAR({self.max_length})" if self.max_length else "VARCHAR"


class TextField(Field):
    """Unlimited length text field."""

    def sql(self):
        return "TEXT"
