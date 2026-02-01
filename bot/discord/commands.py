import os
import asyncio
import discord
from discord.ext import commands
from discord.sinks import WaveSink # TODO: remove if not needed
from bot.discord.sink import PCMSink
from stt.audio_queue import audio_queue

class DiscordVoice(commands.Cog):
    def __init__(self, bot: commands.Bot, save_audio: bool):
        self.bot = bot
        self.save_audio = save_audio
        self.is_recording = False

    @commands.command()
    async def join(self, ctx):
        if not ctx.author.voice or not ctx.author.voice.channel:
            await ctx.send("❌ Nie jesteś na kanale voice.")
            return

        if ctx.voice_client:
            await ctx.send("⚠️ Bot już jest na kanale voice.")
            return

        channel = ctx.author.voice.channel
        vc = await channel.connect(reconnect=True)

        await asyncio.sleep(0.5)

        if not vc.is_connected():
            await ctx.send("❌ Nie udało się połączyć z kanałem voice.")
            return

        await ctx.send("🎙️ Bot dołączył do kanału voice.")
        
    @commands.command()
    async def record(self, ctx):
        vc = ctx.voice_client
        if not vc:
            await ctx.send("❌ Bot nie jest na kanale voice.")
            return

        sink = PCMSink()
        vc.start_recording(sink, self.finished_callback, ctx)

        await ctx.send("🎙️ Realtime STT started.")


    async def finished_callback(self, sink, ctx):
        os.makedirs("recordings", exist_ok=True)

        for user_id, audio in sink.audio_data.items():
            if self.save_audio:
                with open(f"recordings/{user_id}.wav", "wb") as f:
                    print(f"💾 Zapisano nagranie użytkownika {user_id} do recordings/{user_id}.wav")
                    f.write(audio.file.read())

        self.is_recording = False
        await ctx.send("⏹️ Nagrywanie zakończone.")

    @commands.command()
    async def stop(self, ctx):
        vc = ctx.voice_client
        if not vc or not self.is_recording:
            await ctx.send("⚠️ Bot nie nagrywa.")
            return
        audio_queue.put(None)
        vc.stop_recording()
        await ctx.send("⏹️ Nagrywanie zatrzymane.")

    @commands.command()
    async def leave(self, ctx):
        vc = ctx.voice_client
        if not vc:
            await ctx.send("❌ Bot nie jest na kanale voice.")
            return

        await vc.disconnect()
        await ctx.send("👋 Bot opuścił kanał voice.")


def setup(bot: commands.Bot, save_audio: bool):
    bot.add_cog(DiscordVoice(bot, save_audio))
