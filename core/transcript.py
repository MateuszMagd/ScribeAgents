
from pathlib import Path
from typing import TextIO
from datetime import datetime
from constants import FOLDER_TEXT_FILES


from schemas.user import User

class TranscriptWriter:
    def __init__(self,
        base_dir: Path = FOLDER_TEXT_FILES,
        user: User = None,
        session_id: str = None
    ):
        self.base_dir: Path = base_dir
        self.user: User = user
        self.session_id: str = session_id
        self.file_path: Path = self._build_filename(user.id) if user and session_id else None
        
        if not self.file_path:
            raise ValueError("User and session_id must be provided to initialize TranscriptWriter.")
        
        self.file_handler: TextIO = open(self.file_path, "a", encoding="utf-8") if self.file_path else None
        
        if not self.file_handler:
            raise IOError(f"Failed to open file for writing: {self.file_path}")
        
        self.is_closed = False
        
    def write(self, timestamp: datetime, user_id: int, text: str) -> None:
        if self.is_closed:
            raise IOError("Cannot write to closed TranscriptWriter.")
        
        if not self.file_handler:
            raise IOError("File handler is not initialized.")
        
        ts = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        full_line = f"[{ts}] User {user_id}: {text}\n"
        self.file_handler.write(full_line)
        self.file_handler.flush()
    
    def close(self) -> None:
        if not self.is_closed:
            self.file_handler.close()
            self.is_closed = True
    
    def _build_filename(self, user_id: int) -> Path:
        """Build a filename for the transcript based on user ID and session ID."""
        safe_name = self._sanitize(f"user_{user_id}")
        
        return self.base_dir / f"{safe_name}_{self.session_id}.txt"
    
    @staticmethod
    def _sanitize(name: str) -> str:
        """Sanitize the filename to remove or replace unsafe characters."""
        return "".join(c for c in name.lower() if c.isalnum() or c in (' ', '_')).strip()[:32]