from argparse import ArgumentParser

from constants import AVAILABLE_PLATFORM_LIST
from core.session.manager import SessionMenager


def main():
    parser = ArgumentParser(description="Runs a transcription bot on the selected platform.")
    parser.add_argument('--platform_name', type=str, choices=AVAILABLE_PLATFORM_LIST, required=True)
    parser.add_argument('--save_audio', action='store_true')
    args = parser.parse_args()

    manager = SessionMenager()

    if args.platform_name == "discord":
        from bot.discord.client import create_discord_bot, run_discord_bot
        bot = create_discord_bot()
        run_discord_bot(bot, args.save_audio, manager)


if __name__ == '__main__':
    main()