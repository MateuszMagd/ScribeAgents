import discord
import numpy as np

from core.audio.preprocessing import DISCORD_SAMPLE_RATE
from core.session.manager import SessionMenager


class PCMSink(discord.sinks.Sink):
    """Receives raw PCM from Discord and forwards it to the session manager."""

    # Required by pycord 2.8 SinkEventRouter — no events to register.
    __sink_listeners__: list = []

    def __init__(self, manager: SessionMenager):
        super().__init__()
        self.manager = manager

    def walk_children(self):
        """No child sinks."""
        return iter([])

    def write(self, data, user):
        # In pycord 2.8, data is a VoiceData object; user may be None
        if user is None:
            return
        pcm: bytes = data.pcm if hasattr(data, "pcm") else bytes(data)
        if not pcm:
            return
        samples = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)
        samples /= 32768.0
        if samples.size % 2 == 0:
            samples = samples.reshape(-1, 2).mean(axis=1)
        self.manager.buffer_audio(user.id, samples, DISCORD_SAMPLE_RATE)

    def cleanup(self):
        pass
