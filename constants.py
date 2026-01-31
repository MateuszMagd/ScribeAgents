from pathlib import Path

AVAILABLE_PLATFORM_LIST = [
    "discord",
]

FOLDER_TEXT_FILES = Path(__file__).parent / "text_files"
FOLDER_TEXT_FILES.mkdir(exist_ok=True)