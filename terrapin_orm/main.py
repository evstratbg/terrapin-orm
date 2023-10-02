from .connection import PoolManager
from .table import Table

from dataclasses import dataclass
from typing import List


@dataclass
class DatabaseConfig:
    engine: str
    host: str
    port: int
    name: str
    user: str
    password: str
    alias: str = "default"


@dataclass
class OrmConfig:
    databases: List[DatabaseConfig]


class TerrapinORM:
    @classmethod
    async def init(cls, config: OrmConfig):
        aliases = {db.alias for db in config.databases}
        for subclass in Table.__subclasses__():
            if subclass.config.db_alias not in aliases:
                raise ValueError(
                    f"Table {subclass.__name__} db_alias `{subclass.Config.db_alias}` which is not present in config"
                )
        for db in config.databases:
            await PoolManager.add_pool(
                username=db.user,
                password=db.password,
                host=db.host,
                port=db.port,
                database=db.name,
            )
