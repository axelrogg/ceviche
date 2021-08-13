from importlib.util import find_spec
from ceviche.storage.ddriver import DatabaseDriver
from ceviche.exceptions import MissingDatabaseDriver


def check_driver_is_installed(driver: DatabaseDriver) -> bool:
    if find_spec(driver) is None:
        raise MissingDatabaseDriver(f"{driver.capitalize()} is not installed.")
    return True
