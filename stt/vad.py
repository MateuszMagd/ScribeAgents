# stt/vad.py
import torch
import numpy as np

class VoiceActivityDetector:
    def __init__(self, sample_rate=16000, threshold=0.2):
        self.model, _ = torch.hub.load(
            repo_or_dir="snakers4/silero-vad",
            model="silero_vad",
            trust_repo=True
        )
        self.sample_rate = sample_rate
        self.threshold = threshold

        # Silero requirements
        self.frame_size = 512  # for 16kHz
        self.buffer = np.zeros(0, dtype=np.float32)

    def is_speech(self, samples: np.ndarray) -> bool:
        """
        samples: np.ndarray float32 [-1, 1], ANY length
        """
        self.buffer = np.concatenate([self.buffer, samples])

        if len(self.buffer) < self.frame_size:
            return False  # not enough data yet

        frame = self.buffer[: self.frame_size]
        self.buffer = self.buffer[self.frame_size :]

        frame_t = torch.from_numpy(frame).unsqueeze(0)

        with torch.no_grad():
            prob = self.model(frame_t, self.sample_rate).item()

        return prob > self.threshold
