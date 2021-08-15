from pydantic import BaseModel


class DatabaseCredentials(BaseModel):
    host: str
    name: str
    pwrd: str
    user: str
