from cows.db import db
from cows.models import Cow


async def read_one(id: int):
    query = Cow.select().filter(Cow.c.id == id)
    cow = await db.fetch_one(query)
    return cow


async def read_all(**filters) -> list:
    filter_expressions = [
        getattr(Cow.c, k) == v for k, v in filters.items() if v is not None
    ]
    query = Cow.select().where(*filter_expressions)
    cows = await db.fetch_all(query)
    return cows


async def create(cow_values: dict) -> int:
    cow_id = await db.execute(Cow.insert().values(cow_values))
    return cow_id


async def delete(cow_id: int):
    query = Cow.delete().filter(Cow.c.id == cow_id)
    await db.execute(query)


async def update(cow_id: int, cow_values: dict):
    query = Cow.update().where(Cow.c.id == cow_id).values(**cow_values)
    await db.execute(query)
