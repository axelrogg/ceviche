from typing import Dict

from pydantic import BaseModel, root_validator
from sqlalchemy import Table
from uuid import UUID


DatabaseUrl = str
DatabaseTables = Dict[str, Table]


class UserID(BaseModel):
    value: str

    @classmethod
    @root_validator(pre=True)
    def check_user_id_is_valid_uuid_str(cls, values):
        try:
            UUID(values.get("user_id"))
        except ValueError:
            raise ValueError("Invalid UserID format.")
