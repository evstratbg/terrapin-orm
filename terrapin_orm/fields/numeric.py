from .base import BaseIndexedField


class SmallIntField(BaseIndexedField):
    """-32768 to +32767."""

    def sql(self):
        return "SMALLINT"


class IntField(BaseIndexedField):
    """-2147483648 to +2147483647."""

    def sql(self):
        return "INTEGER"


class BigIntField(BaseIndexedField):
    """-9223372036854775808 to +9223372036854775807."""

    def sql(self):
        return "BIGINT"


class DecimalField(BaseIndexedField):
    """Up to 131072 digits before the decimal point; up to 16383 digits after the decimal point."""

    def sql(self):
        return "DECIMAL"


class NumericField(BaseIndexedField):
    """Up to 131072 digits before the decimal point; up to 16383 digits after the decimal point."""

    def sql(self):
        return "NUMERIC"


class RealField(BaseIndexedField):
    """6 decimal digits precision."""

    def sql(self):
        return "REAL"


class DoublePrecisionField(BaseIndexedField):
    """15 decimal digits precision."""

    def sql(self):
        return "DOUBLE PRECISION"


class SmallSerialField(BaseIndexedField):
    """1 to 32767."""

    def sql(self):
        return "SMALLSERIAL NOT NULL PRIMARY KEY"


class SerialField(BaseIndexedField):
    """1 to 2147483647."""

    def sql(self):
        return "SERIAL NOT NULL PRIMARY KEY"


class BigSerialField(BaseIndexedField):
    """1 to 9223372036854775807."""

    def sql(self):
        return "BIGSERIAL NOT NULL PRIMARY KEY"
