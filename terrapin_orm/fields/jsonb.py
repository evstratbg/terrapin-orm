from .base import IndexedField
from .operations import GetJson, GetValue, HasKey


class JSONBField(IndexedField):
    """Binary JSON data structure field."""

    def sql(self):
        return "JSONB"

    # def __get__(self, instance, owner):
    #     return owner.__dict__[self.name]

    def index_sql(self, table_name: str, column_name: str):
        if self.index:
            return f"CREATE INDEX idx_{table_name}_{column_name} ON {table_name} USING GIN ({column_name});"
        return ""

    def has_key(self, key: str):
        return HasKey(self.name, key)

    def get_json(self, key: str):
        return GetJson(self.name, key)

    def get_value(self, key):
        return GetValue(self.name, key)
