from datetime import datetime

from .base import IndexedField


class DateField(IndexedField):
    """Date field (year, month, day)."""

    def sql(self):
        return "DATE"

    def python_type(self):
        return datetime.date


class TimeField(IndexedField):
    """Time field without time zone."""

    def sql(self):
        return "TIME"

    def python_type(self):
        return datetime.time


class TimeWithTimeZoneField(IndexedField):
    """Time field with time zone."""

    def sql(self):
        return "TIME WITH TIME ZONE"

    def python_type(self):
         return datetime


class TimestampField(IndexedField):
    """Timestamp field without time zone."""

    def sql(self):
        return "TIMESTAMP"

    def python_type(self):
         return datetime


class TimestampWithTimeZoneField(IndexedField):
    """Timestamp field with time zone."""

    def sql(self):
        return "TIMESTAMP WITH TIME ZONE"

    def python_type(self):
         return datetime


class IntervalField(IndexedField):
    """Time interval field."""

    def sql(self):
        return "INTERVAL"

    def python_type(self):
         return datetime.timedelta

