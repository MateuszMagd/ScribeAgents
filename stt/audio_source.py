# stt/audio_source.py
import subprocess
import numpy as np
import os

def wav_frames(path, frame_ms=100, target_sr=16000):
    abs_path = os.path.abspath(path)
    print("Loading WAV via ffmpeg:", abs_path)

    frame_size = target_sr * frame_ms // 1000

    cmd = [
        "ffmpeg",
        "-i", abs_path,
        "-f", "s16le",
        "-ac", "1",
        "-ar", str(target_sr),
        "-"
    ]

    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        bufsize=10**8
    )

    bytes_per_sample = 2  # s16le
    bytes_per_frame = frame_size * bytes_per_sample

    while True:
        raw = process.stdout.read(bytes_per_frame)
        if len(raw) < bytes_per_frame:
            break

        frame = np.frombuffer(raw, dtype=np.int16).astype(np.float32)
        frame /= 32768.0  # normalize to [-1, 1]

        yield frame
