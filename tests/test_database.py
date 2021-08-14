from .mock_database import (
    Database,
    DatabaseClient,
    DatabaseCredential,
    DatabaseDriver,
    DB_HOST,
    DB_PWRD,
    DB_USER,
    DDriver,
    MetaData,
    MockDatabase,
    MOCK_DB_NAME
)


ddriver = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.asyncpg)
cred = DatabaseCredential(dbhost=DB_HOST, dbname=MOCK_DB_NAME, dbpwrd=DB_PWRD, dbuser=DB_USER)
meta = MetaData()
DB = Database(ddriver, cred, meta, is_async=True)


class TestOperations(MockDatabase):

    def test_db_create(self):
        pass