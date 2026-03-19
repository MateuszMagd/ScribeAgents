import logging
import sys
from pathlib import Path

_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s — %(message)s"
_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

_LOG_DIR = Path(__file__).parent.parent.parent / "logs"


def setup_logging(log_dir: Path = _LOG_DIR) -> None:
    """Configure root logger with a console handler and a file handler."""
    log_dir.mkdir(exist_ok=True)

    formatter = logging.Formatter(_LOG_FORMAT, datefmt=_DATE_FORMAT)

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    file_handler = logging.FileHandler(log_dir / "scribe.log", encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    root = logging.getLogger()
    root.setLevel(logging.DEBUG)
    root.addHandler(console_handler)
    root.addHandler(file_handler)


def get_logger(name: str) -> logging.Logger:
    """Return a named logger."""
    return logging.getLogger(name)
