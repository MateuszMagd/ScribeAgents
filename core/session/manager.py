import datetime
from pathlib import Path

import numpy as np

from constants import FOLDER_TEXT_FILES
from core.logging.logger import get_logger
from schemas.user import User
from core.audio.audio_to_text import audio_to_text
from core.transcript.transcript import Transcript

_log = get_logger(__name__)


class SessionMenager:
    def __init__(self):
        self.sessions: dict[int, tuple[User, Transcript]] = {}
        self._entries: list[dict] = []

    def create_session(self, user_data: User):
        """Register a user for the current recording session."""
        transcript_for_user = Transcript(
            path=FOLDER_TEXT_FILES,
            file_name=f"{user_data.name}.{user_data.id}.txt",
        )
        self.sessions[user_data.id] = (user_data, transcript_for_user)
        _log.info("Session created for user %s (id=%d)", user_data.name, user_data.id)

    def get_session(self, session_id: int) -> tuple[User, Transcript] | None:
        """Return user data and transcript for the given session id, or None."""
        return self.sessions.get(session_id)

    def delete_session(self, session_id: int):
        """Remove a user from the active sessions."""
        if session_id in self.sessions:
            del self.sessions[session_id]
            _log.debug("Session deleted for user id=%d", session_id)

    def handle_audio(
        self,
        user_id: int,
        audio: np.ndarray,
        sample_rate: int,
    ):
        """Transcribe an audio chunk and persist the result for the given user."""
        session = self.get_session(user_id)
        if session is None:
            return

        user, transcript = session

        text = audio_to_text(audio, sample_rate)
        if not text:
            _log.debug("Empty transcription for user id=%d — skipping", user_id)
            return

        _log.debug("Transcribed for user id=%d: %s", user_id, text)

        transcript.add_entry(user.display_name or user.name, text)

    def get_transcript_path(self, session_id: int):
        """Return the transcript file path for the given session id, or None."""
        session = self.get_session(session_id)
        if session is None:
            return None
        _, transcript = session
        return transcript.path

    def finalize(self):
        """Close all active sessions and log completion."""
        _log.info("Finalizing session with %d user(s)", len(self.sessions))
        self.sessions.clear()