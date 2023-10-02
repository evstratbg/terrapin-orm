from .base import IndexedField


class DateField(IndexedField):
    """Date field (year, month, day)."""

    def sql(self):
        return "DATE"


class TimeField(IndexedField):
    """Time field without time zone."""

    def sql(self):
        return "TIME"


class TimeWithTimeZoneField(IndexedField):
    """Time field with time zone."""

    def sql(self):
        return "TIME WITH TIME ZONE"


class TimestampField(IndexedField):
    """Timestamp field without time zone."""

    def sql(self):
        return "TIMESTAMP"


class TimestampWithTimeZoneField(IndexedField):
    """Timestamp field with time zone."""

    def sql(self):
        return "TIMESTAMP WITH TIME ZONE"


class IntervalField(IndexedField):
    """Time interval field."""

    def sql(self):
        return "INTERVAL"
