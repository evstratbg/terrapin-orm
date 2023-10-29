from .fields.base import Field
from .sql import SQLManager
from .table import Table


def select(*columns: Field):
    return SQLManager().select(*columns)


def update(table: type[Table]):
    return SQLManager(table)


def delete(table: type[Table]):
    return SQLManager(table).delete()


def insert_into(table: type[Table]):
    return SQLManager(table)

