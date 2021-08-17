from ceviche.storage.database import DatabaseDriver


driver_map = {
    "postgresql": {
        "async": [DatabaseDriver.asyncpg],
        "sync": [DatabaseDriver.psycopg2]
    }
}