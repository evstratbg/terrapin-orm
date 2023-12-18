from .configs import DatabaseConfig
from .connection import PoolManager
from .table import Table


class TerrapinORM:
    @classmethod
    async def init(cls, *configs: DatabaseConfig):
        aliases = {db.alias for db in configs}
        for subclass in Table.__subclasses__():
            db_alias = subclass.config.db_alias
            if subclass.config.abstract:
                continue
            if db_alias not in aliases:
                raise ValueError(
                    f"Table {subclass.__name__} db_alias "
                    f"`{db_alias}` which is not present in config",
                )
        for cfg in configs:
            await PoolManager.add_pool(
                alias=cfg.alias,
                username=cfg.user,
                password=cfg.password,
                host=cfg.host,
                port=cfg.port,
                database=cfg.name,
            )
