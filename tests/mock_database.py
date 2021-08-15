from os import getenv
from unittest import TestCase

from sqlalchemy import MetaData, text
from ceviche import (
    Database,
    DatabaseClient,
    DatabaseCredentials,
    DatabaseDriver,
    DDriver
)


DB_HOST = getenv("POSTGRES_HOST")
DB_NAME = getenv("POSTGRES_DB")
DB_PWRD = getenv("POSTGRES_PWRD")
DB_USER = getenv("POSTGRES_USER")

DDRIVER = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.psycopg2)
CRED = DatabaseCredentials(host=DB_HOST, name=DB_NAME, password=DB_PWRD, user=DB_USER)
META = MetaData()
DB = Database(DDRIVER, CRED, META)
ENGINE = DB.engine()

MOCK_DB_NAME = "mock_database"


class MockDatabase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:

        conn = ENGINE.connect()

        # drop mock database if it exists
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {MOCK_DB_NAME}"))
        except Exception as e:
            print(e)

        # create mock database
        try:
            conn.execute(text(f"CREATE DATABASE {MOCK_DB_NAME}"))
        except Exception as e:
            print(e)

    @classmethod
    def tearDownClass(cls) -> None:

        conn = ENGINE.connect()

        # drop mock database
        try:
            conn.execute(text(f"DROP DATABASE {MOCK_DB_NAME}"))
        except Exception as e:
            print(e)
