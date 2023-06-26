import sqlalchemy
from databases import Database

from cows.consts import COW_API_DATABASE_URL

db = Database(COW_API_DATABASE_URL)

dialect = sqlalchemy.dialects.postgresql.dialect()
metadata = sqlalchemy.MetaData()
