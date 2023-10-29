from .base import IndexedField


class BooleanField(IndexedField):
    """Boolean field (true or false)."""

    def sql(self):
        return "BOOLEAN"

    def python_type(self):
        return bool
