from .base import IndexedField


class ByteaField(IndexedField):
    """Binary data field."""

    def sql(self):
        return "BYTEA"
