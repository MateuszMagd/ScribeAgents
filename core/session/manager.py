import datetime
from pathlib import Path

import numpy as np

from constants import FOLDER_TEXT_FILES
from schemas.user import User
from core.audio.audio_to_text import audio_to_text


class SessionMenager:
    def __init__(self):
        self.sessions: dict[int, User] = {}
        self._entries: list[dict] = []

    def create_session(self, user_data: User):
        """Register a user for the current recording session."""
        self.sessions[user_data.id] = user_data

    def get_session(self, session_id: int) -> User | None:
        """Return user data for the given session id, or None."""
        return self.sessions.get(session_id)

    def delete_session(self, session_id: int):
        """Remove a user from the active sessions."""
        if session_id in self.sessions:
            del self.sessions[session_id]

    def handle_audio(
        self,
        user_id: int,
        audio: np.ndarray,
        sample_rate: int,
        timestamp: datetime.datetime,
    ):
        """Transcribe an audio chunk and persist the result for the given user."""
        user = self.get_session(user_id)
        if user is None:
            return

        text = audio_to_text(audio, sample_rate)
        if not text:
            return

        entry = {
            "user_id": user_id,
            "username": user.display_name or user.name,
            "text": text,
            "timestamp": timestamp,
        }
        self._entries.append(entry)
        self._write_entry(entry)

    def _write_entry(self, entry: dict):
        """Append a single transcript line to the user's per-session file."""
        FOLDER_TEXT_FILES.mkdir(exist_ok=True)
        path = FOLDER_TEXT_FILES / f"{entry['user_id']}.txt"
        line = f"[{entry['timestamp'].isoformat()}] {entry['text']}\n"
        with open(path, "a", encoding="utf-8") as f:
            f.write(line)

    def finalize(self) -> str:
        """Merge all entries into one chronological transcript file and return it."""
        if not self._entries:
            return ""

        sorted_entries = sorted(self._entries, key=lambda e: e["timestamp"])
        lines = [
            f"[{e['timestamp'].isoformat()}] {e['username']}: {e['text']}"
            for e in sorted_entries
        ]
        transcript = "\n".join(lines)

        FOLDER_TEXT_FILES.mkdir(exist_ok=True)
        filename = f"transcript_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(FOLDER_TEXT_FILES / filename, "w", encoding="utf-8") as f:
            f.write(transcript)

        return transcript