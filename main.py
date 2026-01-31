from argparse import ArgumentParser
from constants import AVAILABLE_PLATFORM_LIST


def main():
    parser = ArgumentParser(description="Command-line tool for deciding what platform you gonna run bots.")
    parser.add_argument('--platform_name', type=str, choices=AVAILABLE_PLATFORM_LIST, help='Your platform name', required=True)
    args = parser.parse_args()
    
    print("Your platform name is:", args.platform_name)
    
    if args.platform_name == "discord":
        from bot.discord.client import create_discord_bot, run_discord_bot
        bot = create_discord_bot()
        run_discord_bot(bot)

if __name__ == '__main__':
    main()