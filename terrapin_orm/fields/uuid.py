from .base import IndexedField


class UUIDField(IndexedField):
    """Universal Unique Identifier field."""

    def sql(self):
        return "UUID"
