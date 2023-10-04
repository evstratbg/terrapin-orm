from dataclasses import dataclass
from typing import List


@dataclass
class TableConfig:
    table_name: str
    db_alias: str
    abstract: bool = False


@dataclass
class DatabaseConfig:
    host: str
    port: int
    name: str
    user: str
    password: str
    alias: str = "default"


@dataclass
class OrmConfig:
    databases: List[DatabaseConfig]



__all__ = ("TableConfig", "OrmConfig", "DatabaseConfig")
