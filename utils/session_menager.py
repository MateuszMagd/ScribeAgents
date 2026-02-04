from schemas.user import User
from datetime import datetime

class SessionMenager:
    def __init__(self):
        pass
    
    def start(self) -> None:
        """Start a new session."""
        pass
    
    def stop(self) -> None:
        """End the current session."""
        pass
    
    def register_user(self, user: User) -> None:
        """Register a new user in the session."""
        pass
    
    def append_transcript(self, user_id: int, transcript: str, timestamp: datetime) -> None:
        """Append a transcript to the user's session."""
        pass
    
    def finalize(self) -> None:
        """Finalize and save the session data."""
        pass