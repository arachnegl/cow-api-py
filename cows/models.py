"""Contains the models of the app.

"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import create_engine
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import String
from sqlalchemy import Table

from cows.consts import COW_API_DATABASE_URL
from cows.db import db
from cows.schemas import CowSchemaPost
from cows.schemas import CowSchemaPut


metadata = MetaData()


CowTable = Table(
    "cow",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column("name", String),
    Column("sex", String),
    Column("birthdate", DateTime),
    Column("condition", String),
    Column("has_calves", Boolean),
    Column("feeding_amount_kg", Integer),
    Column("feeding_cron_schedule", String),
    Column("feeding_last_measured", DateTime),
    Column("weight_mass_kg", Integer),
    Column("weight_last_measured", DateTime),
    Column("milk_production_last_milk", DateTime),
    Column("milk_production_cron_schedule", String),
    Column("milk_production_amount_l", Integer),
)


engine = create_engine(COW_API_DATABASE_URL)
metadata.create_all(engine)


async def db_cow_get_one(id: int):
    query = CowTable.select().filter(CowTable.c.id == id)
    cow = await db.fetch_one(query)
    return cow


async def db_cow_get_list() -> list:
    query = CowTable.select()
    cows = await db.fetch_all(query)
    return cows


def flatten(a: dict, prefix="") -> dict:
    res = {}
    for k, v in a.items():
        if isinstance(v, dict):
            nested = flatten(v, prefix=f"{k}_")
            for fk, fv in nested.items():
                res[fk] = fv
        else:
            res[f"{prefix}{k}"] = v
    return res


async def db_cow_create(cow: CowSchemaPost) -> int:
    cow_id = await db.execute(CowTable.insert().values(flatten(cow.dict())))
    return cow_id


async def db_cow_delete(cow_id: int):
    query = CowTable.delete().filter(CowTable.c.id == cow_id)
    await db.execute(query)


async def db_cow_update(cow: CowSchemaPut) -> int:
    cow_id = await db.execute(CowTable.insert().values(flatten(cow.dict())))
    return cow_id
