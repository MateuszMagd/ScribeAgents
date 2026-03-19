from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class Platform(str, Enum):
    """All available platforms."""
    DISCORD = "discord"

class User(BaseModel):
    """Represents a user in the system."""
    id: int
    name: str
    display_name: Optional[str]
    bot: bool
    roles: List[str]
    joined_at: str
    
