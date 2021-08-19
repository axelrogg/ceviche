from enum import Enum
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

from ceviche.types import DatabaseTables, DatabaseUrl
from ceviche.storage.models import __get_autoloaded_database_tables


class DatabaseCredentials(BaseModel):
    host:     str
    name:     str
    password: str
    user:     str

    class Config:
        allow_mutation = False


class DatabaseClient(str, Enum):
    postgresql = "postgresql"


class DatabaseDriver(str, Enum):
    asyncpg = "asyncpg"
    psycopg2 = "psycopg2"


class DDriver(BaseModel):
    client: DatabaseClient
    driver: DatabaseDriver

    class Config:
        allow_mutation = False


class Database:

    def __init__(
            self,
            ddriver: DDriver,
            credentials: DatabaseCredentials,
            metadata: MetaData,
            tabls: Optional[DatabaseTables] = None,
            is_async: bool = False
    ) -> None:
        self.ddriver = ddriver
        self.metadata = metadata
        self.tabls = tabls
        self.is_async = is_async
        self.__dbname = credentials.name
        self.__dbhost = credentials.host
        self.__dbpwrd = credentials.password
        self.__dbuser = credentials.user
        self.__url = self.__set_url()

    def tables(self, engine: Engine) -> Optional[DatabaseTables]:
        if self.tabls:
            return self.tabls
        autoloaded_tables = __get_autoloaded_database_tables(self.metadata, engine)
        return autoloaded_tables

    def engine(self, **kwargs) -> Engine:
        engine = create_engine(self.__url, **kwargs)
        if self.is_async:
            engine = create_async_engine(self.__url, **kwargs)
        return engine

    def __set_url(self) -> DatabaseUrl:
        client = self.ddriver.client
        driver = self.ddriver.driver
        return f"{client}+{driver}://{self.__dbuser}:{self.__dbpwrd}@{self.__dbhost}/{self.__dbname}"
