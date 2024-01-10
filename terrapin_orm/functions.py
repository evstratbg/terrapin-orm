from .fields.base import Field
from .managers import (
    CreateTableSQLManager,
    DeleteSQLManager,
    DropTableSQLManager,
    InsertSQLManager,
    ReturningUpdateSQLManager,
    SelectSQLManager,
    UpdateSQLManager,
)
from .table import _T


def select(*columns: Field) -> SelectSQLManager[_T]:
    return SelectSQLManager(
        columns=columns,
        select_for_update=False,
        nowait=False,
        skip_locked=False,
    )


def select_for_update(*columns: Field, nowait: bool, skip_locked: bool) -> SelectSQLManager[_T]:
    return SelectSQLManager(
        columns=columns,
        select_for_update=True,
        nowait=nowait,
        skip_locked=skip_locked,
    )


def update(table: type[_T]) -> UpdateSQLManager[_T] | ReturningUpdateSQLManager[_T]:
    return UpdateSQLManager(table)


def delete(table: type[_T]) -> DeleteSQLManager[_T]:
    return DeleteSQLManager(table)


def insert_into(table: type[_T]) -> InsertSQLManager[_T]:
    return InsertSQLManager(table)


def create_table(table: type[_T]) -> CreateTableSQLManager[_T]:
    return CreateTableSQLManager(table)


def drop_table(table: type[_T]) -> DropTableSQLManager[_T]:
    return DropTableSQLManager(table)
