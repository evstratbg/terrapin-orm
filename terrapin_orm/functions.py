from .fields.base import Field
from .sql import SQLManager
from .table import Table


def select(*columns: Field):
    return SQLManager().select(*columns)


def select_for_update(*columns: Field, nowait: bool, skip_locked: bool):
    return SQLManager().select_for_update(*columns, nowait=nowait, skip_locked=skip_locked)


def update(table: type[Table]):
    return SQLManager(table)


def delete(table: type[Table]):
    return SQLManager(table).delete()


def insert_into(table: type[Table]):
    return SQLManager(table)


def create_table(table: type[Table]):
    return SQLManager(table).create_table()


def drop_table(table: type[Table]):
    return SQLManager(table).drop_table()
