from datetime import datetime
class SaveText:
    def __init__(self, filepath: str):
        self.filepath = filepath

    def save(self, text: str):
        with open(self.filepath, 'a', encoding='utf-8') as f:
            f.write(f"{datetime.now()}: {text}\n")