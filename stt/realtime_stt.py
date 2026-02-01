# stt/realtime_stt.py
import torch
from stt.vad import VoiceActivityDetector
from stt.chunker import AudioChunker
from stt.whisper_engine import WhisperEngine
from stt.audio_source import wav_frames
from utils.text import SaveText

def run_stt(audio_source, on_text):
    vad = VoiceActivityDetector()
    chunker = AudioChunker(
        min_speech_ms=200,
        min_silence_ms=300
    )
    whisper_engine = WhisperEngine("small", language="pl")

    for frame_np in audio_source:
        is_speech = vad.is_speech(frame_np)
        chunk = chunker.process(frame_np, is_speech)

        if chunk is not None:
            text = whisper_engine.transcribe(chunk)
            if text:
                on_text(text)
