from datetime import datetime
from constants import FOLDER_TEXT_FILES

class SaveText:
    def __init__(self, filepath: str):
        self.filepath = FOLDER_TEXT_FILES / filepath

    def save(self, text: str):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()}: {text}\n")