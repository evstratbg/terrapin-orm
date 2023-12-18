### ORM Fields for PostgreSQL

A very lightweight asynchronous ORM for PostgreSQL that is very close to SQL standard

## Usage

```python
import random
import asyncio

from terrapin_orm.configs import DatabaseConfig, TableConfig
from terrapin_orm.fields.jsonb import JSONBField
from terrapin_orm.fields.numeric import IntField
from terrapin_orm.functions import delete, insert_into, select, update, create_table, drop_table
from terrapin_orm.main import TerrapinORM
from terrapin_orm.table import Table


# creating a table
class Users(Table):
    id = IntField(pk=True)
    age = IntField()
    jsonb = JSONBField()

    config = TableConfig(
        table_name="users",
        db_alias="default",
    )

# creating a config
config = DatabaseConfig(
    host="localhost",
    port=5432,
    name="postgres",
    user="postgres",
    password="postgres",
)


async def main():
    # initing orm
    await TerrapinORM.init(config)
    
    # creating a table
    await create_table(Users)

    # selecting a set of columns
    await select(Users.id).from_(Users).where(Users.id == 1)
    
    # selecting all columns
    await select().from_(Users).where(Users.id == 1)
    
    # updating columns using += value and filters
    await update(Users).set(age=Users.age + 10).where(age=Users.age + 10)
    
    # updating columns with the given values and filters
    await update(Users).set(age=10).where(Users.age > 10, age=Users.age + 10)
    
    # deleting rows using filtering
    await delete(Users).where(Users.id == 2)
    
    # inserting values
    await insert_into(Users).values(id=10, age=10)
    
    # dropping a table
    await drop_table(Users)


if __name__ == "__main__":
    asyncio.run(main())

```

TODO:

1) Joins
2) Migrations
3) raw_sql
4) Tests

