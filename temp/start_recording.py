import datetime
import sys
from pathlib import Path

# Add project root to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import sounddevice as sd

from core.session.manager import SessionMenager
from schemas.user import User

SAMPLE_RATE = 16000   # Hz — required by Whisper
CHUNK_SECONDS = 5     # length of each audio chunk in seconds
USER_ID = 1


def record_and_transcribe(duration_seconds: int = 30):
    """Record microphone audio in chunks and forward each to SessionMenager."""
    manager = SessionMenager()

    user = User(
        id=USER_ID,
        name="LocalTest",
        display_name="Local Test",
        bot=False,
        roles=["member"],
        joined_at=datetime.datetime.now().isoformat(),
    )
    manager.create_session(user)

    total_chunks = max(1, duration_seconds // CHUNK_SECONDS)
    print(f"Recording for {duration_seconds}s in {CHUNK_SECONDS}s chunks ({total_chunks} total)...")
    print("Speak into the microphone. Press Ctrl+C to stop early.\n")

    try:
        for i in range(total_chunks):
            print(f"[Chunk {i + 1}/{total_chunks}] Recording...")
            chunk = sd.rec(
                frames=CHUNK_SECONDS * SAMPLE_RATE,
                samplerate=SAMPLE_RATE,
                channels=1,
                dtype="float32",
                blocking=True,
            )
            audio = chunk.flatten()
            manager.handle_audio(
                user_id=USER_ID,
                audio=audio,
                sample_rate=SAMPLE_RATE,
            )
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    manager.delete_session(USER_ID)



if __name__ == "__main__":
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    record_and_transcribe(duration)