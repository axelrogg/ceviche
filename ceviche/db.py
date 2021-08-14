from os import getenv
from sqlalchemy import MetaData
from ceviche.storage.database import Database, DatabaseCredential
from ceviche.storage.ddriver import DatabaseClient, DatabaseDriver, DDriver


dbhost = getenv("POSTGRES_HOST")
dbname = getenv("POSTGRES_DB")
dbpwrd = getenv("POSTGRES_PWRD")
dbuser = getenv("POSTGRES_USER")


ddriver = DDriver(client=DatabaseClient.postgresql, driver=DatabaseDriver.asyncpg)
cred = DatabaseCredential(dbhost=dbhost, dbname=dbname, dbpwrd=dbpwrd, dbuser=dbuser)

_meta = MetaData()

_db = Database(ddriver, cred, _meta, tables=None, is_async=True)
db_engine = _db.gen_engine()
db_tables = _db.show_tables()
