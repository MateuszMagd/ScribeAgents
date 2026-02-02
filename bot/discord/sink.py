from discord.sinks.core import Sink
import numpy as np
from stt.temp_stt import SimpleSTT

stt = SimpleSTT()

class PCMSink(Sink):
    def write(self, data, user):
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        samples /= 32768.0

        # stereo → mono
        samples = samples.reshape(-1, 2).mean(axis=1)

        stt.process(samples)
