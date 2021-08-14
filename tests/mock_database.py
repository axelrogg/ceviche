from os import getenv
from unittest import TestCase

from sqlalchemy import MetaData, text
from ceviche.storage.database import Database, DatabaseCredential
from ceviche.storage.ddriver import DatabaseClient, DatabaseDriver, DDriver


class MockDatabase(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        dbhost = getenv("POSTGRES_HOST")
        dbname = getenv("POSTGRES_DB")
        dbpwrd = getenv("POSTGRES_PWRD")
        dbuser = getenv("POSTGRES_USER")

        ddriver = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.psycopg2)
        meta = MetaData()
        cred = DatabaseCredential(dbhost=dbhost, dbname=dbname, dbpwrd=dbpwrd, dbuser=dbuser)
        db = Database(ddriver, cred, meta)
        engine = db.gen_engine()

        mock_db_name = "mock_database"

        conn = engine.connect()
        # drop the mock database if it exists
        try:
            conn.execute(text(f"DROP DATABASE IF EXISTS {mock_db_name}"))
        except Exception as e:
            print(e)
        # create the mock database
        try:
            conn.execute(text(f"CREATE DATABASE {mock_db_name}"))
        except Exception as e:
            print(e)



