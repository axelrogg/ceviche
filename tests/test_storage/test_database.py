from .mock_database import (
    Database,
    DatabaseClient,
    DatabaseCredentials,
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
cred = DatabaseCredentials(host=DB_HOST, name=MOCK_DB_NAME, pwrd=DB_PWRD, user=DB_USER)
meta = MetaData()
DB = Database(ddriver, cred, meta, is_async=True)


class TestDatabaseOperations(MockDatabase):

    def test_db_create(self):
        pass