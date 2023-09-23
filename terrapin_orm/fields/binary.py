from .base import BaseField


class ByteaField(BaseField):
    """Binary data field."""

    def sql(self):
        return "BYTEA"
