# stt/whisper_engine.py
import whisper
import numpy as np

class WhisperEngine:
    def __init__(self, model_name="small", language="pl", task="transcribe"):
        self.model = whisper.load_model(model_name)
        self.language = language
        self.task = task

    def transcribe(self, audio_np: np.ndarray):
        result = self.model.transcribe(
            audio_np,
            language=self.language,
            task=self.task,
            fp16=False
        )
        return result["text"].strip()
