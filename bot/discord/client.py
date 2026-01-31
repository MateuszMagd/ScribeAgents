import os
import discord
import asyncio

from discord.ext import commands
from bot.discord.commands import setup

from dotenv import load_dotenv

load_dotenv()

def create_discord_bot() -> commands.Bot:
    asyncio.set_event_loop(asyncio.new_event_loop())

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot


def run_discord_bot(bot: commands.Bot, save_audio: bool):
    setup(bot, save_audio)

    @bot.event
    async def on_ready():
        print(f"🤖 Discord bot zalogowany jako {bot.user}")

    TOKEN = os.getenv("TOKEN")
    bot.run(TOKEN)
