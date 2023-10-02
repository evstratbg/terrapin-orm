from .base import PkField


class SmallIntField(PkField):
    """-32768 to +32767."""

    def sql(self):
        sql = "SMALLINT"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class IntField(PkField):
    """-2147483648 to +2147483647."""

    def sql(self):
        sql = "INTEGER"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class BigIntField(PkField):
    """-9223372036854775808 to +9223372036854775807."""

    def sql(self):
        sql = "BIGINT"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class DecimalField(PkField):
    """Up to 131072 digits before the decimal point; up to 16383 digits after the decimal point."""

    def sql(self):
        sql = "DECIMAL"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class NumericField(PkField):
    """Up to 131072 digits before the decimal point; up to 16383 digits after the decimal point."""

    def sql(self):
        sql = "NUMERIC"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class RealField(PkField):
    """6 decimal digits precision."""

    def sql(self):
        sql = "REAL"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class DoublePrecisionField(PkField):
    """15 decimal digits precision."""

    def sql(self):
        sql = "DOUBLE PRECISION"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class SmallSerialField(PkField):
    """1 to 32767."""

    def sql(self):
        sql = "SMALLSERIAL NOT NULL"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class SerialField(PkField):
    """1 to 2147483647."""

    def sql(self):
        sql = "SERIAL NOT NULL"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql


class BigSerialField(PkField):
    """1 to 9223372036854775807."""

    def sql(self):
        sql = "BIGSERIAL NOT NULL"
        if self.pk:
            sql += " PRIMARY KEY"
        return sql
