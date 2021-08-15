from os import getenv
from sqlalchemy import MetaData
from ceviche import (
    Database,
    DatabaseClient,
    DatabaseCredentials,
    DatabaseDriver,
    DDriver,
    get_default_tables,
)


dbhost = getenv("POSTGRES_HOST")
dbname = getenv("POSTGRES_DB")
dbpwrd = getenv("POSTGRES_PWRD")
dbuser = getenv("POSTGRES_USER")


ddriver = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.asyncpg)
cred = DatabaseCredentials(host=dbhost, name=dbname, pwrd=dbpwrd, user=dbuser)

_meta = MetaData()

_db = Database(ddriver, cred, _meta, tabls=get_default_tables(_meta), is_async=True)
db_engine = _db.engine()
db_tables = _db.tables()
