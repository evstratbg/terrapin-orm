from .base import PkField


class UUIDField(PkField):
    """Universal Unique Identifier field."""

    def sql(self):
        return "UUID" if not self.pk else "UUID PRIMARY KEY"
