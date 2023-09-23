from .base import BaseIndexedField


class DateField(BaseIndexedField):
    """Date field (year, month, day)."""

    def sql(self):
        return "DATE"


class TimeField(BaseIndexedField):
    """Time field without time zone."""

    def sql(self):
        return "TIME"


class TimeWithTimeZoneField(BaseIndexedField):
    """Time field with time zone."""

    def sql(self):
        return "TIME WITH TIME ZONE"


class TimestampField(BaseIndexedField):
    """Timestamp field without time zone."""

    def sql(self):
        return "TIMESTAMP"


class TimestampWithTimeZoneField(BaseIndexedField):
    """Timestamp field with time zone."""

    def sql(self):
        return "TIMESTAMP WITH TIME ZONE"


class IntervalField(BaseIndexedField):
    """Time interval field."""

    def sql(self):
        return "INTERVAL"
