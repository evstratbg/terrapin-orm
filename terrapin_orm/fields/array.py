from .base import ArrayField


class SmallIntArrayField(ArrayField):
    """Array of small-range integers."""

    def __init__(self):
        super().__init__(item_type="SMALLINT")

    def index_sql(self, table_name: str, column_name: str):
        if self.index:
            return f"CREATE INDEX idx_{table_name}_{column_name} ON {table_name} USING GIN ({column_name});"
        return ""


class IntArrayField(ArrayField):
    """Array of integers."""

    def __init__(self):
        super().__init__(item_type="INTEGER")


class BigIntArrayField(ArrayField):
    """Array of large-range integers."""

    def __init__(self):
        super().__init__(item_type="BIGINT")


class DecimalArrayField(ArrayField):
    """Array of decimals."""

    def __init__(self):
        super().__init__(item_type="DECIMAL")


class NumericArrayField(ArrayField):
    """Array of numeric values."""

    def __init__(self):
        super().__init__(item_type="NUMERIC")


class RealArrayField(ArrayField):
    """Array of real numbers."""

    def __init__(self):
        super().__init__(item_type="REAL")


class DoublePrecisionArrayField(ArrayField):
    """Array of double precision numbers."""

    def __init__(self):
        super().__init__(item_type="DOUBLE PRECISION")


class VarcharArrayField(ArrayField):
    """Array of variable-length character strings."""

    def __init__(self):
        super().__init__(item_type="VARCHAR")


class TextAreaField(ArrayField):
    """Array of text."""

    def __init__(self):
        super().__init__(item_type="TEXT")


class ByteaArrayField(ArrayField):
    """Array of binary data."""

    def __init__(self):
        super().__init__(item_type="BYTEA")


class DateArrayField(ArrayField):
    """Array of dates."""

    def __init__(self):
        super().__init__(item_type="DATE")


class TimeArrayField(ArrayField):
    """Array of times without time zones."""

    def __init__(self):
        super().__init__(item_type="TIME")


class TimeWithTimeZoneArrayField(ArrayField):
    """Array of times with time zones."""

    def __init__(self):
        super().__init__(item_type="TIME WITH TIME ZONE")


class TimestampArrayField(ArrayField):
    """Array of timestamps without time zones."""

    def __init__(self):
        super().__init__(item_type="TIMESTAMP")


class TimestampWithTimeZoneArrayField(ArrayField):
    """Array of timestamps with time zones."""

    def __init__(self):
        super().__init__(item_type="TIMESTAMP WITH TIME ZONE")


class BooleanArrayField(ArrayField):
    """Array of boolean values."""

    def __init__(self):
        super().__init__(item_type="BOOLEAN")


class UUIDArrayField(ArrayField):
    """Array of UUIDs."""

    def __init__(self):
        super().__init__(item_type="UUID")
