from pydantic import BaseModel, Field
from typing import Optional

class User(BaseModel):
    id: int = Field(..., description="The unique identifier for the user")
    displayname: str = Field(... , max_length=100, description="The full name of the user")
    username: Optional[str] = Field(None, min_length=3, max_length=50, description="The username of the user")
    
    
    