from core.adapters.basic import PlatformAdapter


class DiscordAdapter(PlatformAdapter):
    """Manages recording lifecycle for a Discord voice channel."""

    def __init__(self, voice_client, manager, sink):
        self.voice_client = voice_client
        self.manager = manager
        self._sink = sink

    async def start_listening(self):
        """Start recording from the voice channel."""
        self.voice_client.start_recording(self._sink, self._on_finished)

    async def _on_finished(self, sink, *args):
        pass

    async def stop(self):
        """Stop recording from the voice channel."""
        self.voice_client.stop_recording()