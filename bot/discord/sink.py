import numpy as np
from discord.sinks.core import Sink

from core.session.manager import SessionMenager

DISCORD_SAMPLE_RATE = 48000


class PCMSink(Sink):
    def __init__(self, manager: SessionMenager):
        super().__init__()
        self.manager = manager

    def write(self, data, user):
        """Convert raw PCM from Discord and forward to the manager."""
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        samples /= 32768.0
        samples = samples.reshape(-1, 2).mean(axis=1)
        self.manager.handle_audio(user.id, samples, DISCORD_SAMPLE_RATE)
