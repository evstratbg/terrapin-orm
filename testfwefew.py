from .fields.base import BaseField, BaseArrayField


class BaseTable:
    """Base class for database tables."""

    table_name = None

    def sql(self):
        """Generate SQL statement to create the table."""
        if not self.table_name:
            raise ValueError("Table name must be defined!")

        fields = {k: v for k, v in self.__class__.__dict__.items() if isinstance(v, (BaseField, BaseArrayField))}

        field_definitions = ", ".join([f"{name} {field.sql()}" for name, field in fields.items()])

        return f"CREATE TABLE {self.table_name} ({field_definitions});"
