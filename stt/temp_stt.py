import numpy as np

from stt.vad import VoiceActivityDetector
from stt.chunker import AudioChunker
from stt.whisper_engine import WhisperEngine
from utils.text import SaveText
import librosa

class SimpleSTT:
    def __init__(self, file_path: str = "transcriptions.txt"):
        self.whisper = WhisperEngine("small", language="pl", task="transcribe")
        self.save_text = SaveText(file_path)
        self.buffer = []
        self.silence_frames = 0
        self.min_silence_frames = 20  # ~500 ms

    def process(self, frame_np):
        rms = np.sqrt(np.mean(frame_np ** 2))

        if rms < 0.01:
            self.silence_frames += 1
        else:
            self.silence_frames = 0

        self.buffer.append(frame_np)

        if self.silence_frames < self.min_silence_frames:
            print("⏳ Still speaking, silence frames:", self.silence_frames)
            return

        audio_so_far = np.concatenate(self.buffer)

        # minimum ~1 sec speech (48kHz)
        if len(audio_so_far) < 48000:
            print("⚠️ Ignoring short chunk, len:", len(audio_so_far))
            self.buffer.clear()
            return

        print("🔥 Sending chunk to Whisper, len:", len(audio_so_far))

        # RESAMPLING
        audio_16k = librosa.resample(audio_so_far, orig_sr=48000, target_sr=16000)

        text = self.whisper.transcribe(audio_16k)
        if text:
            print("🗣️", text)
            self.save_text.save(text)

        self.buffer.clear()
        self.silence_frames = 0
