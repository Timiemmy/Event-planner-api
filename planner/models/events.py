from pydantic import BaseModel
#from sqlmodel import SQLModel, Field, Column,JSON
from beanie import Document
from typing import List, Optional


# SQL DB
"""
class Event(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    image: str
    description: str
    tags: List[str] = Field(sa_column=Column(JSON))
    location: str
    


    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            
            "example": {
                "title": "FastApi Book",
                "image": "http://example.com/image.jpg",
                "description": "This is a sample event.",
                "tags": ["sample", "event"],
                "location": "Google Meet",
                
            }
        }
"""

# Mongo NOSQL
class Event(Document):
    creator: Optional[str]
    title: str
    image: str
    description: str
    tags: List[str]
    location: str
   
    


    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            
            "example": {
                "creator": "John Doe",
                "title": "FastApi Book",
                "image": "http://example.com/image.jpg",
                "description": "This is a sample event.",
                "tags": ["sample", "event"],
                "location": "Google Meet",
                
            }
        }
    class Settings:
        name= 'events'


class EventUpdate(BaseModel):
    title: Optional[str]
    image: Optional[str]
    description: Optional[str]
    tags: Optional[List[str]]
    location: Optional[str]


    class Config:
        json_schema_extra = {
            "example": {
                "title": "FastApi Book",
                "image": "http://example.com/image.jpg",
                "description": "This is a sample event.",
                "tags": ["sample", "event"],
                "location": "Google Meet",

            }
        }