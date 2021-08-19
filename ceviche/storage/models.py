from sqlalchemy import Column, DateTime, MetaData, String, Table, Text, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.engine import Engine

from ceviche.types import DatabaseTables


def get_default_tables(metadata: MetaData) -> DatabaseTables:

    tables = {
        "user_account": Table(
            "user_account", metadata,
            Column("user_id", UUID, primary_key=True, nullable=False),
            Column("username", String(50), unique=True, nullable=False),
            Column("email", String(254), unique=True, nullable=False),
            Column("password", Text, nullable=False),
            Column("created_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP")),
            Column("last_updated_at", DateTime(timezone=True), nullable=False, server_default=text("CURRENT_TIMESTAMP"))
        ),
    }

    return tables


def __get_autoloaded_database_tables(metadata: MetaData, engine: Engine) -> DatabaseTables:
    default_tables = get_default_tables(metadata)
    # override default tables by loaded tables.
    default_tables["user_account"] = Table("user_account", metadata, autoload_with=engine)
    # TODO: override more default tables.

    return default_tables
