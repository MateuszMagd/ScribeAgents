import numpy as np

from core.adapters.basic import PlatformAdapter
from core.audio.preprocessing import DISCORD_SAMPLE_RATE
from core.session.manager import SessionMenager
from discord.voice_client import VoiceClient


class DiscordAdapter(PlatformAdapter):
    """Manages recording lifecycle for a Discord voice channel."""

    def __init__(self, voice_client: VoiceClient, manager: SessionMenager, sink):
        self.voice_client: VoiceClient = voice_client
        self.manager: SessionMenager = manager
        self._sink = sink

    async def start_listening(self):
        """Start recording from the voice channel."""
        self.voice_client.start_recording(self._sink, self._on_finished)

    async def _on_finished(self, sink, *args):
        pass

    async def stop(self):
        """Stop recording from the voice channel."""
        self.voice_client.stop_recording()
        
    async def _write(self, data, user):
        """Convert raw PCM from Discord and forward to the manager."""
        samples = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        samples /= 32768.0
        samples = samples.reshape(-1, 2).mean(axis=1)
        self.manager.handle_audio(user.id, samples, DISCORD_SAMPLE_RATE)
