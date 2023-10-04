from .connection import PoolManager
from .table import Table
from .configs import OrmConfig


class TerrapinORM:
    @classmethod
    async def init(cls, config: OrmConfig):
        aliases = {db.alias for db in config.databases}
        for subclass in Table.__subclasses__():
            db_alias = subclass.config.db_alias
            if db_alias not in aliases:
                raise ValueError(
                    f"Table {subclass.__name__} db_alias "
                    f"`{db_alias}` which is not present in config",
                )
        for db in config.databases:
            await PoolManager.add_pool(
                username=db.user,
                password=db.password,
                host=db.host,
                port=db.port,
                database=db.name,
            )
