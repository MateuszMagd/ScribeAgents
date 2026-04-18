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
        self._audio_buffers: dict[int, list[np.ndarray]] = {}
        self._buffer_sample_rates: dict[int, int] = {}

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

    def buffer_audio(self, user_id: int, samples: np.ndarray, sample_rate: int):
        """Accumulate audio samples for a user to be transcribed on finalize."""
        if user_id not in self.sessions:
            return
        if user_id not in self._audio_buffers:
            self._audio_buffers[user_id] = []
            self._buffer_sample_rates[user_id] = sample_rate
        self._audio_buffers[user_id].append(samples)

    def flush_buffers(self):
        """Transcribe all buffered audio and append results to transcripts."""
        for user_id, chunks in self._audio_buffers.items():
            if not chunks:
                continue
            session = self.get_session(user_id)
            if session is None:
                continue
            user, transcript = session
            audio = np.concatenate(chunks)
            sample_rate = self._buffer_sample_rates.get(user_id, 48000)
            text = audio_to_text(audio, sample_rate)
            if text:
                transcript.add_entry(user.display_name or user.name, text)
                _log.debug("Transcribed for user id=%d: %s", user_id, text)
            else:
                _log.debug("Empty transcription for user id=%d — skipping", user_id)
        self._audio_buffers.clear()
        self._buffer_sample_rates.clear()

    def get_transcript_path(self, session_id: int):
        """Return the transcript file path for the given session id, or None."""
        session = self.get_session(session_id)
        if session is None:
            return None
        _, transcript = session
        return transcript.path

    def finalize(self):
        """Flush buffered audio, close all active sessions and log completion."""
        _log.info("Finalizing session with %d user(s)", len(self.sessions))
        self.flush_buffers()
        self.sessions.clear()