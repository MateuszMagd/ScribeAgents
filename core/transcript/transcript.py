from pathlib import Path

from datetime import datetime

from core.logging.logger import get_logger

_log = get_logger(__name__)


class Transcript:
    """Manages a per-user transcript file for a recording session."""

    def __init__(self, path: str, file_name: str):
        self.path = Path(path) / file_name
        self.file_name = file_name
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.create_file()

    def add_entry(self, user_name: str, text: str):
        """Append a timestamped entry to the transcript file."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] | {user_name}: {text}\n"
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(entry)
        _log.debug("Entry added for user '%s': %s", user_name, text)

    def create_file(self):
        """Create the transcript file with a header."""
        starting_entry = f"Transcript started at: {self.start_time}\n\n"
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(starting_entry)
        _log.info("Transcript file created: %s", self.path)