from pathlib import Path

from datetime import datetime

class Transcript:
    def __init__(self, path: str, file_name: str):
        self.path = Path(path) / file_name
        self.file_name = file_name
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print("Creating transcript file at:", self.path)
        
        self.create_file()
    
    def add_entry(self, user_name: str, text: str):
        print(f"Adding entry to transcript for user '{user_name}': {text}")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = f"[{timestamp}] | {user_name}: {text}\n"
        with open(self.path, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def create_file(self):
        starting_entry = f"Transcript started at: {self.start_time}\n\n"
        
        with open(self.path, 'w', encoding='utf-8') as f:
            f.write(starting_entry)