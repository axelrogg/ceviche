from typing import Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.util._collections import FacadeDict           # noqa

from ceviche.storage import DatabaseTables, DatabaseUrl
from ceviche.storage.ddriver import DatabaseDriver, DDriver
from ceviche.storage.credentials import DatabaseCredentials
from ceviche.storage.check_driver_is_installed import check_driver_is_installed


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
        self.__url = self.__set_db_url()

    def tables(self) -> Optional[DatabaseTables]:
        if self.tabls:
            return self.tabls
        return self.__reflect_db()

    def engine(self, force_sync_engine: bool = False, override_url: Optional[DatabaseUrl] = None, **kwargs) -> Engine:
        url = override_url or self.__url
        engine = create_engine(url, **kwargs)
        if self.is_async and not force_sync_engine:
            engine = create_async_engine(url, **kwargs)
        return engine

    def __reflect_db(self) -> Optional[DatabaseTables]:
        # reflection can only be performed on a non-async engine
        engine = self.engine()

        if self.is_async:
            # TODO: right now we generate a new url for a sync driver for postgresql.  This needs to be automatic
            # by mapping sync and async drivers to the corresponding client.
            tmp_url = self.__set_db_url(DatabaseDriver.psycopg2)
            # create a sync engine
            engine = self.engine(force_sync_engine=True, override_url=tmp_url)
        result = self.metadata.reflect(bind=engine)

        if isinstance(result, FacadeDict):
            return dict(result)
        return None

    def __set_db_url(self, override_driver: Optional[DatabaseDriver] = None) -> DatabaseUrl:
        client = self.ddriver.client
        driver = self.ddriver.driver
        if override_driver and check_driver_is_installed(override_driver.name):
            driver = override_driver.name
        return f"{client}+{driver}://{self.__dbuser}:{self.__dbpwrd}@{self.__dbhost}/{self.__dbname}"
