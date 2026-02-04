from pydantic import BaseModel, Field
from typing import Optional
from schemas.user import User

class SessionMeta(BaseModel):
    session_id: str = Field(..., description="The unique identifier for the session")
    platform: str = Field(..., description="The platform where the session is hosted")
    started_at: Optional[str] = Field(None, description="The timestamp when the session started")
    ended_at: Optional[str] = Field(None, description="The timestamp when the session ended")
    participants: list[User] = Field(..., description="List of users participating in the session")