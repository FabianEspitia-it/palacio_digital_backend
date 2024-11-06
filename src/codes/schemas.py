from pydantic import BaseModel


class SessionCodes(BaseModel):
    email: str
    password: str
