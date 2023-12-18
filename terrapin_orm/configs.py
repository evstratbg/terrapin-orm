from dataclasses import dataclass


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


__all__ = ("TableConfig", "DatabaseConfig")
