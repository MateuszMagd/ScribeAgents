from datetime import datetime

from schemas.user import User
from schemas.session_meta import SessionMeta
from utils.audio import AudioWriter


class SessionManager:
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
    
    def append_audio(self, user_id: int, audio_data: bytes) -> None:
        """Append audio data to the user's session."""
        pass
    def finalize(self) -> None:
        """Finalize and save the session data."""
        pass