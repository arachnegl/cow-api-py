import os

# DATABASE_URL = "postgresql+asyncpg://username:password@localhost/cow_db"
COW_API_DATABASE_URL = os.environ.get(
    "COW_API_DATABASE_URL", "postgresql://username:password@localhost/cow_db"
)
