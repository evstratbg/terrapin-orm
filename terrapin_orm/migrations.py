import asyncpg

from .fields import TimestampField, VarcharField
from .table import Table


class Terrapin(Table):
    name = VarcharField(max_length=255, index=True)
    applied_at = TimestampField()


async def generate_migration_script():
    conn = await asyncpg.connect()

    # Проверка наличия поля city в реальной таблице
    exists = await conn.fetchrow("""
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = 'usertable' AND column_name = 'city';""",
    )

    # Если поля city нет, создаем SQL-запрос для добавления
    if not exists:
        return """
        ALTER TABLE usertable ADD COLUMN city VARCHAR(255);
        CREATE INDEX idx_usertable_city ON usertable (city);
        """
    else:
        print("Field 'city' already exists in the table.")  # noqa: T201

    await conn.close()
    return None
