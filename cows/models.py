"""Contains the models of the app.

"""
from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table

from cows.db import metadata

Cow = Table(
    "cow",
    metadata,
    Column(
        "id",
        Integer,
        primary_key=True,
        autoincrement=True,
    ),
    Column("name", String),
    Column("sex", String),  # TODO implement as ENUM
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
