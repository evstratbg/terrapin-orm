from .fields.base import BaseField, BaseIndexedField


class BaseTable:
    """Base class for database tables."""

    _config = None

    def sql(self):
        """Generate SQL statement to create the table."""
        table_name = self.__class__.__name__.lower()
        if self._config and self._config.get("table_name"):
            table_name = self._config["table_name"]

        fields = {
            k: v
            for k, v in self.__class__.__dict__.items()
            if isinstance(v, BaseField)
        }

        field_definitions = []
        field_indexes = []
        for name, field in fields.items():
            field_definitions.append(f"{name} {field.sql()}")
            if isinstance(field, BaseIndexedField) and field.index:
                field_indexes.append(
                    field.index_sql(table_name, name),
                )

        field_definitions = ",\n\t".join(field_definitions)
        field_indexes = "\n".join(field_indexes)

        return f"CREATE TABLE IF NOT EXISTS {table_name} ({field_definitions});\n{field_indexes}"
