from .base import BaseArrayField


class SmallIntArrayField(BaseArrayField):
    """Array of small-range integers."""

    def __init__(self):
        super().__init__(item_type="SMALLINT")


class IntegerArrayField(BaseArrayField):
    """Array of integers."""

    def __init__(self):
        super().__init__(item_type="INTEGER")


class BigIntArrayField(BaseArrayField):
    """Array of large-range integers."""

    def __init__(self):
        super().__init__(item_type="BIGINT")


class DecimalArrayField(BaseArrayField):
    """Array of decimals."""

    def __init__(self):
        super().__init__(item_type="DECIMAL")


class NumericArrayField(BaseArrayField):
    """Array of numeric values."""

    def __init__(self):
        super().__init__(item_type="NUMERIC")


class RealArrayField(BaseArrayField):
    """Array of real numbers."""

    def __init__(self):
        super().__init__(item_type="REAL")


class DoublePrecisionArrayField(BaseArrayField):
    """Array of double precision numbers."""

    def __init__(self):
        super().__init__(item_type="DOUBLE PRECISION")


class VarcharArrayField(BaseArrayField):
    """Array of variable-length character strings."""

    def __init__(self):
        super().__init__(item_type="VARCHAR")


class TextAreaField(BaseArrayField):
    """Array of text."""

    def __init__(self):
        super().__init__(item_type="TEXT")


class ByteaArrayField(BaseArrayField):
    """Array of binary data."""

    def __init__(self):
        super().__init__(item_type="BYTEA")


class DateArrayField(BaseArrayField):
    """Array of dates."""

    def __init__(self):
        super().__init__(item_type="DATE")


class TimeArrayField(BaseArrayField):
    """Array of times without time zones."""

    def __init__(self):
        super().__init__(item_type="TIME")


class TimeWithTimeZoneArrayField(BaseArrayField):
    """Array of times with time zones."""

    def __init__(self):
        super().__init__(item_type="TIME WITH TIME ZONE")


class TimestampArrayField(BaseArrayField):
    """Array of timestamps without time zones."""

    def __init__(self):
        super().__init__(item_type="TIMESTAMP")


class TimestampWithTimeZoneArrayField(BaseArrayField):
    """Array of timestamps with time zones."""

    def __init__(self):
        super().__init__(item_type="TIMESTAMP WITH TIME ZONE")


class BooleanArrayField(BaseArrayField):
    """Array of boolean values."""

    def __init__(self):
        super().__init__(item_type="BOOLEAN")


class UUIDArrayField(BaseArrayField):
    """Array of UUIDs."""

    def __init__(self):
        super().__init__(item_type="UUID")
