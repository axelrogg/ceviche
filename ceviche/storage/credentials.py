from pydantic import BaseModel


class DatabaseCredentials(BaseModel):
    host:     str
    name:     str
    password: str
    user:     str
