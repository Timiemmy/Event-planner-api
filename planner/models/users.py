from pydantic import BaseModel, EmailStr
from typing import Optional, List
from beanie import Document, Link
from .events import Event


class User(Document):
    email: EmailStr
    password: str
    events: List[Link[Event]]

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "John_Doe1343",
                "events":[]
            }
        }
        


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


