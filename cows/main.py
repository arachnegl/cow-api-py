import logging

import sqlalchemy
from fastapi import FastAPI

from cows.db import db
from cows.db import dialect
from cows.db import metadata
from cows.routes import router


log = logging.Logger(name=__name__)

version = "0.0.1"


description = """
# Cows API

## cow endpoints

Please find below the various endpoints.
You are encouraged to try out the endpoints.

## Warning

This is a pre prod and as such there will be unimplemented edge cases.
Do file a PR if you come across some.
"""

app = FastAPI(
    title="cows",
    description=description,
    version=version,
)


@app.on_event("startup")
async def startup():
    await db.connect()

    for table in metadata.tables.values():
        schema = sqlalchemy.schema.CreateTable(table, if_not_exists=True)
        query = str(schema.compile(dialect=dialect))
        await db.execute(query=query)

    log.info("db connected")


@app.on_event("shutdown")
async def shutdown():
    await db.disconnect()
    log.error("db disconnected")


app.include_router(router)
