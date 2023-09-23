from .base import BaseField


class UUIDField(BaseField):
    """Universal Unique Identifier field."""

    def sql(self):
        return "UUID"
