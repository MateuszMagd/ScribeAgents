import warnings

import numpy as np

from core.adapters.basic import PlatformAdapter
from core.audio.preprocessing import DISCORD_SAMPLE_RATE
from core.session.manager import SessionMenager
from discord.voice.client import VoiceClient
from bot.discord.sink import PCMSink


class DiscordAdapter(PlatformAdapter):
    """Manages recording lifecycle for a Discord voice channel."""

    def __init__(self, voice_client: VoiceClient, manager: SessionMenager, sink: PCMSink):
        self.voice_client: VoiceClient = voice_client
        self.manager: SessionMenager = manager
        self._sink = sink

    async def start_listening(self):
        """Start recording from the voice channel."""
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", RuntimeWarning)
            self.voice_client.start_recording(self._sink, self._on_finished)

    async def _on_finished(self, sink, *args):
        pass

    async def stop(self):
        """Stop recording from the voice channel."""
        self.voice_client.stop_recording()
