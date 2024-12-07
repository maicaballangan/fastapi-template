from pydantic import BaseModel
from pydantic import EmailStr
from sqlmodel import Field


# Generic message
class Message(BaseModel):
    message: str


# JSON payload containing access token
class Token(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class Email(BaseModel):
    email: EmailStr = Field(max_length=100)
