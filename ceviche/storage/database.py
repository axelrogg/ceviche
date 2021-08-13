from typing import Optional

from pydantic import BaseModel
from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

from ceviche.storage import DatabaseTables, DatabaseUrl
from ceviche.storage.ddriver import DatabaseDriver, DDriver


class DatabaseCredential(BaseModel):
    dbhost: str
    dbname: str
    dbpwrd: str
    dbuser: str


class Database:

    def __init__(
            self,
            ddriver: DDriver,
            credential: DatabaseCredential,
            metadata: MetaData,
            tables: Optional[DatabaseTables] = None,
            is_async: bool = False
    ) -> None:
        self.ddriver = ddriver
        self.metadata = metadata
        self.tables = tables
        self.is_async = is_async
        self.__dbname = credential.dbname
        self.__dbhost = credential.dbhost
        self.__dbpwrd = credential.dbpwrd
        self.__dbuser = credential.dbuser
        self.__url = self.__set_db_url()

    def show_tables(self) -> DatabaseTables:
        if self.tables:
            return self.tables
        return self.__reflect_db()

    def gen_engine(self, override_url: Optional[DatabaseUrl] = None, is_async: bool = False, **kwargs) -> Engine:
        url = override_url or self.__url
        engine = create_engine(url, **kwargs)
        if is_async:
            engine = create_async_engine(url, **kwargs)
        return engine

    def __reflect_db(self) -> DatabaseTables:
        # reflection can only be performed on a non-async engine
        if not self.is_async:
            engine = self.gen_engine()
        else:
            # TODO: right now we generate a new url for a sync driver for postgresql.  This needs to be automatic
            # by mapping sync and async drivers to the corresponding client.
            tmp_url = self.__set_db_url(DatabaseDriver.psycopg2)
            # create a sync engine
            engine = self.gen_engine(tmp_url)
        result = self.metadata.reflect(bind=engine)
        return dict(result)

    def __set_db_url(self, override_driver: Optional[DatabaseDriver] = None) -> DatabaseUrl:
        client = self.ddriver.client
        driver = override_driver.name or self.ddriver.driver
        return f"{client}+{driver}://{self.__dbuser}:{self.__dbpwrd}@{self.__dbhost}/{self.__dbname}"
