from sqlalchemy import Column, DateTime, MetaData, String, Table, Text, text
from sqlalchemy.dialects.postgresql import UUID

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
