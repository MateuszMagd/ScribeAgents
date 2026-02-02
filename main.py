import threading

from argparse import ArgumentParser
from constants import AVAILABLE_PLATFORM_LIST
from stt.realtime_stt import run_stt
from stt.audio_queue import audio_generator

from utils.text import SaveText

text_saver = SaveText("text_files/transcriptions.txt")

# Temp here
def handle_transcript(text: str):
    print("🗣️", text)
    text_saver.save(text)



def main():
    parser = ArgumentParser(description="Command-line tool for deciding what platform you gonna run bots.")
    parser.add_argument('--platform_name', type=str, choices=AVAILABLE_PLATFORM_LIST, help='Your platform name', required=True)
    parser.add_argument('--save_audio', action='store_true', help='Flag to save audio files')
    args = parser.parse_args()
    
    print("Your platform name is:", args.platform_name)
    print("Save audio flag is set to:", args.save_audio)
    
    if args.platform_name == "discord":
        from bot.discord.client import create_discord_bot, run_discord_bot
        
        bot = create_discord_bot()
        run_discord_bot(bot, args.save_audio)

if __name__ == '__main__':
    print("Starting the application...")
    main()
    print("Application finished.")