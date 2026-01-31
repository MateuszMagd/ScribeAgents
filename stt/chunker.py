# stt/chunker.py
import numpy as np

class AudioChunker:
    def __init__(
        self,
        sample_rate=16000,
        min_speech_ms=300,
        min_silence_ms=500,
        overlap_ms=200
    ):
        self.sample_rate = sample_rate
        self.min_speech_samples = sample_rate * min_speech_ms // 1000
        self.min_silence_samples = sample_rate * min_silence_ms // 1000
        self.overlap_samples = sample_rate * overlap_ms // 1000

        self.buffer = []
        self.silence = 0
        self.speech_samples = 0
        self.active = False

    def process(self, frame, is_speech):
        self.buffer.append(frame)

        if is_speech:
            self.speech_samples += len(frame)
            self.silence = 0
            self.active = True
        else:
            if self.active:
                self.silence += len(frame)

        if (
            self.active
            and self.speech_samples >= self.min_speech_samples
            and self.silence >= self.min_silence_samples
        ):
            chunk = np.concatenate(self.buffer)
            keep = chunk[-self.overlap_samples :]
            self.buffer = [keep]
            self.active = False
            self.speech_samples = 0
            self.silence = 0
            return chunk

        return None
