from discord.sinks.core import Sink
import numpy as np
from stt.audio_queue import audio_queue

class PCMSink(Sink):
    def __init__(self):
        super().__init__()

    def write(self, data, user):
        # data: bytes PCM 48kHz stereo s16le
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        samples /= 32768.0

        # stereo -> mono
        samples = samples.reshape(-1, 2).mean(axis=1)

        audio_queue.put(samples)
