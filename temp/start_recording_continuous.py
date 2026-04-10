import datetime
import sys
import queue
import threading
from pathlib import Path

# Add project root to path so imports work
sys.path.insert(0, str(Path(__file__).parent.parent))

import numpy as np
import sounddevice as sd
import torch
from silero_vad import load_silero_vad

from core.session.manager import SessionMenager
from schemas.user import User

SAMPLE_RATE = 16000    # Hz — required by Whisper and Silero VAD
BLOCK_SIZE = 512       # callback block size (~32ms at 16kHz)
SILENCE_BLOCKS = 20    # silent blocks before end-of-utterance (~640ms)
MIN_SPEECH_BLOCKS = 5  # minimum utterance length; shorter chunks are ignored
USER_ID = 1


def record_continuously(duration_seconds: int | None = None):
    """Record audio continuously, detect speech via VAD and transcribe."""
    print("Loading VAD model...")
    vad_model = load_silero_vad()
    vad_model.eval()

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

    audio_queue: queue.Queue[np.ndarray] = queue.Queue()
    stop_event = threading.Event()

    def audio_callback(indata, frames, time_info, status):
        audio_queue.put(indata[:, 0].copy())

    def vad_is_speech(block: np.ndarray) -> bool:
        tensor = torch.from_numpy(block).float()
        with torch.no_grad():
            confidence = vad_model(tensor, SAMPLE_RATE).item()
        return confidence > 0.5

    def processing_loop():
        speech_buffer: list[np.ndarray] = []
        silence_count = 0
        in_speech = False
        speech_start_time: datetime.datetime | None = None

        while not stop_event.is_set() or not audio_queue.empty():
            try:
                block = audio_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            is_speech = vad_is_speech(block)

            if is_speech:
                if not in_speech:
                    in_speech = True
                    speech_start_time = datetime.datetime.now()
                    print("[VAD] Speech detected...")
                speech_buffer.append(block)
                silence_count = 0
            else:
                if in_speech:
                    silence_count += 1
                    speech_buffer.append(block)

                    if silence_count >= SILENCE_BLOCKS:
                        if len(speech_buffer) >= MIN_SPEECH_BLOCKS:
                            audio = np.concatenate(speech_buffer)
                            print(f"[VAD] End of utterance ({len(audio) / SAMPLE_RATE:.1f}s) — transcribing...")
                            manager.handle_audio(
                                user_id=USER_ID,
                                audio=audio,
                                sample_rate=SAMPLE_RATE,
                            )
                        speech_buffer = []
                        silence_count = 0
                        in_speech = False

        if speech_buffer and len(speech_buffer) >= MIN_SPEECH_BLOCKS:
            audio = np.concatenate(speech_buffer)
            manager.handle_audio(
                user_id=USER_ID,
                audio=audio,
                sample_rate=SAMPLE_RATE,
            )

    processor = threading.Thread(target=processing_loop, daemon=True)
    processor.start()

    limit = f"for {duration_seconds}s" if duration_seconds else "indefinitely"
    print(f"Recording {limit}. Speak into the microphone. Press Ctrl+C to stop.\n")

    try:
        with sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=1,
            dtype="float32",
            blocksize=BLOCK_SIZE,
            callback=audio_callback,
        ):
            if duration_seconds:
                sd.sleep(duration_seconds * 1000)
            else:
                while True:
                    sd.sleep(1000)
    except KeyboardInterrupt:
        print("\nInterrupted by user.")

    stop_event.set()
    processor.join()

    session_path = manager.get_transcript_path(USER_ID)
    manager.finalize()
    manager.delete_session(USER_ID)

    if session_path and session_path.exists():
        content = session_path.read_text(encoding="utf-8")
        print("\n=== Transcript ===")
        print(content)
    else:
        print("\nNo speech recognized.")


if __name__ == "__main__":
    # Optional argument: total recording duration in seconds (omit for infinite)
    duration = int(sys.argv[1]) if len(sys.argv) > 1 else None
    record_continuously(duration)
