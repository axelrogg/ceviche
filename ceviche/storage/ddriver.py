from enum import Enum
from pydantic import BaseModel


class DatabaseClient(str, Enum):
    postgresql = "postgresql"


class DatabaseDriver(str, Enum):
    asyncpg = "asyncpg"
    psycopg2 = "psycopg2"


class DDriver(BaseModel):
    client: DatabaseClient
    driver: DatabaseDriver
