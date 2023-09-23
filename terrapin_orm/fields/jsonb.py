from .base import BaseField


class JSONBField(BaseField):
    """Binary JSON data structure field."""

    def sql(self):
        return "JSONB"
