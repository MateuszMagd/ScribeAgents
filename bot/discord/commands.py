import asyncio

import discord
from discord.ext import commands

from bot.discord.sink import PCMSink
from core.adapters.discord import DiscordAdapter
from core.logging.logger import get_logger
from core.session.manager import SessionMenager
from schemas.user import User

_log = get_logger(__name__)


class DiscordVoice(commands.Cog):
    def __init__(self, bot: commands.Bot, save_audio: bool, manager: SessionMenager):
        self.bot = bot
        self.save_audio = save_audio
        self.manager = manager
        self.is_recording = False
        self._adapter: DiscordAdapter | None = None

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ You are not in a voice channel.")
            return

        if ctx.voice_client:
            await ctx.send("⚠️ Bot is already in a voice channel.")
            return

        vc = await ctx.author.voice.channel.connect(reconnect=True)

        await asyncio.sleep(0.5)

        if not vc.is_connected():
            await ctx.send("❌ Failed to connect to the voice channel.")
            return

        _log.info("Joined voice channel: %s", ctx.author.voice.channel.name)
        await ctx.send("🎙️ Joined the voice channel.")

    @commands.command()
    async def record(self, ctx):
        if self.is_recording:
            await ctx.send("⚠️ Already recording.")
            return

        vc = ctx.voice_client
        if not vc:
            await ctx.send("❌ Bot is not in a voice channel.")
            return

        for member in ctx.author.voice.channel.members:
            if not member.bot:
                user = User(
                    id=member.id,
                    name=member.name,
                    display_name=member.display_name,
                    bot=member.bot,
                    roles=[role.name for role in member.roles],
                    joined_at=member.joined_at.isoformat() if member.joined_at else "",
                )
                self.manager.create_session(user)

        sink = PCMSink(self.manager)
        self._adapter = DiscordAdapter(vc, self.manager, sink)
        await self._adapter.start_listening()
        self.is_recording = True
        _log.info("Recording started in channel: %s", ctx.author.voice.channel.name)
        await ctx.send("🎙️ Recording started.")

    @commands.command()
    async def stop(self, ctx):
        if not self.is_recording or self._adapter is None:
            await ctx.send("⚠️ Not recording.")
            return

        await self._adapter.stop()
        self.manager.finalize()
        self.is_recording = False
        self._adapter = None
        _log.info("Recording stopped by user: %s", ctx.author.name)
        await ctx.send("⏹️ Recording stopped. Transcript saved.")

    @commands.command()
    async def leave(self, ctx):
        vc = ctx.voice_client
        if vc:
            if self.is_recording and self._adapter:
                await self._adapter.stop()
                self.manager.finalize()
                self.is_recording = False
                self._adapter = None
            await vc.disconnect()
        await ctx.send("👋 Bot left the voice channel.")


def setup(bot: commands.Bot, save_audio: bool, manager: SessionMenager):
    bot.add_cog(DiscordVoice(bot, save_audio, manager))
