import wave
from pathlib import Path

from schemas.user import User

class AudioWriter:
    def __init__(self, 
        base_dir: Path, # Add base dir
        user: User,
        sample_rate: int,
        channels: int,
        sample_width: int,
    ):
        self.base_dir = base_dir
        self.user = user
        self.sample_rate = sample_rate
        self.channels = channels
        self.sample_width = sample_width
        
        self.file_path = self._build_filename(user.id)
        self.wave_handler = wave.open(self.file_path, 'wb')
        self.wave_handler.setnchannels(channels)
        self.wave_handler.setsampwidth(sample_width)
        self.wave_handler.setframerate(sample_rate)
        
        self.is_closed = False
        
    def write(self, audio_data: bytes) -> None:
        if self.is_closed:
            raise IOError("Cannot write to closed AudioWriter.")
        
        if not audio_data:
            return
        
        self.wave_handler.writeframes(audio_data)
        
    def close(self) -> None:
        if not self.is_closed:
            self.wave_handler.close()
            self.is_closed = True
            
    def _build_filename(self, user_id: int) -> Path:
        """Build a filename for the audio file based on user ID."""
        safe_name = self._sanitize(f"user_{user_id}")
        return self.base_dir / f"{safe_name}.wav"
    
    def _sanitize(self, name: str) -> str:
        """Sanitize the filename to remove or replace unsafe characters."""
        return "".join(c for c in name.lower() if c.isalnum() or c in (' ', '_')).strip()[:32]