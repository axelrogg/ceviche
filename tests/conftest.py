from os import getenv

import pytest
from sqlalchemy import MetaData, text, inspect

from ceviche import (
    Database,
    DatabaseClient,
    DatabaseCredentials,
    DatabaseDriver,
    DDriver,
    get_default_tables,
)


class DatabaseSetUpFailure(Exception):
    pass


@pytest.fixture
def get_database_envvars():

    db_creds = {
        "host": getenv("TEST_POSTGRES_HOST"),
        "name": getenv("TEST_POSTGRES_DB"),
        "pwrd": getenv("TEST_POSTGRES_PWRD"),
        "user": getenv("TEST_POSTGRES_USER")
    }

    return db_creds


@pytest.fixture
def database_creds(get_database_envvars):
    creds = DatabaseCredentials(
        host=get_database_envvars["host"],
        name=get_database_envvars["name"],
        password=get_database_envvars["pwrd"],
        user=get_database_envvars["user"]
    )
    return creds
    

@pytest.fixture
def database_ddriver():
    ddriver = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.psycopg2)
    return ddriver


@pytest.fixture
def database_meta():
    meta = MetaData()
    return meta


@pytest.fixture
def database_sync_engine(database_creds, database_ddriver, database_meta):
    db = Database(database_ddriver, database_creds, database_meta)
    engine = db.engine(echo="debug", echo_pool="debug")
    return engine


@pytest.fixture
def database_async_engine(database_creds):
    meta = MetaData()
    ddriver = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.asyncpg)
    db = Database(ddriver, database_creds, meta)
    engine = db.engine(echo="debug", echo_pool="debug")
    return engine


mock_database = "mock_database"


@pytest.fixture(scope="session")
def mock_database(database_engine, database_meta, database_async_engine):

    print("Setting up tests...")
    conn = database_engine.connect()

    # drop mock database if it exists
    try:
        conn.execute(text(f"DROP DATABASE IF EXISTS {mock_database}"))
    except Exception as e:
        print(e)

    # create mock database
    print(f"Creating database {mock_database}...")
    try:
        conn.execute(text(f"CREATE DATABASE {mock_database}"))
    except Exception as e:
        print(e)
    print(f"Database {mock_database}...")

    # create all tables
    tables = get_default_tables(database_meta)
    print(f"Creating all tables in {mock_database}...")
    try:
        for table in tables.values():
            table.create(database_engine)
    except Exception as e:
        print(e)

    # inspect database and check if all tables have been successfully created
    insp = inspect(database_engine)

    table_nos = len(tables.keys())

    table_counter = 0
    for table_name in tables.keys():
        if table_name in insp.get_table_names():
            table_counter += 1
    if table_nos != table_counter:
        raise DatabaseSetUpFailure("Could not create all tables in mock database.")
    print(f"All tables in database {mock_database} were created.")

    print("Setup completed.")

    # create the async engine
    yield database_async_engine

    print("Starting tests teardown.")

    # drop mock database
    print(f"Dropping database {mock_database}...")
    try:
        conn.execute(text(f"DROP DATABASE {mock_database}"))
    except Exception as e:
        print(e)
    print(f"Database {mock_database} was deleted.")

    # clean up database variables created to make the mock database
    del conn
    del database_engine
    del database_meta
    del database_async_engine

    print("Teardown completed")
