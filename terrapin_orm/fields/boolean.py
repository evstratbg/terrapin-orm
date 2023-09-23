from .base import BaseIndexedField


class BooleanField(BaseIndexedField):
    """Boolean field (true or false)."""

    def sql(self):
        return "BOOLEAN"
