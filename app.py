from argparse import ArgumentParser

from constants import AVAILABLE_PLATFORM_LIST
from core.logging.logger import setup_logging, get_logger

setup_logging()
_log = get_logger(__name__)


def main():
    parser = ArgumentParser(description="Runs a transcription bot on the selected platform.")
    parser.add_argument('--platform_name', type=str, choices=AVAILABLE_PLATFORM_LIST, required=True)
    parser.add_argument('--save_audio', action='store_true')
    args = parser.parse_args()

    _log.info("Starting ScribeAgents on platform: %s", args.platform_name)

    if args.platform_name == "discord":
        from bot.discord.client import create_discord_bot, run_discord_bot
        bot = create_discord_bot()
        
        run_discord_bot(bot, args.save_audio)


if __name__ == '__main__':
    main()