from typing import Optional

from sqlalchemy import create_engine, MetaData
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import create_async_engine

from ceviche.storage import DatabaseTables, DatabaseUrl
from ceviche.storage.ddriver import DDriver
from ceviche.storage.credentials import DatabaseCredentials


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

    def tables(self) -> Optional[DatabaseTables]:
        if self.tabls:
            return self.tabls
        return None

    def engine(self, **kwargs) -> Engine:
        engine = create_engine(self.__url, **kwargs)
        if self.is_async:
            engine = create_async_engine(self.__url, **kwargs)
        return engine

    def __set_url(self) -> DatabaseUrl:
        client = self.ddriver.client
        driver = self.ddriver.driver
        return f"{client}+{driver}://{self.__dbuser}:{self.__dbpwrd}@{self.__dbhost}/{self.__dbname}"
