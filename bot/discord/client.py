import os
import discord
import asyncio

from discord.ext import commands
from bot.discord.commands import setup
from core.logging.logger import get_logger

from dotenv import load_dotenv

load_dotenv()

_log = get_logger(__name__)

def create_discord_bot() -> commands.Bot:
    asyncio.set_event_loop(asyncio.new_event_loop())

    intents = discord.Intents.default()
    intents.message_content = True
    intents.voice_states = True

    bot = commands.Bot(command_prefix="!", intents=intents)
    return bot


def run_discord_bot(bot: commands.Bot, save_audio: bool, manager):
    setup(bot, save_audio, manager)

    @bot.event
    async def on_ready():
        _log.info("Bot logged in as %s", bot.user)

    TOKEN = os.getenv("TOKEN")
    bot.run(TOKEN)
