from ceviche.storage.ddriver import DatabaseDriver


drivers_map = {
    "postgresql": {
        "async": [DatabaseDriver.asyncpg],
        "sync": [DatabaseDriver.psycopg2]
    }
}