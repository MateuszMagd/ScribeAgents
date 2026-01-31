# stt/realtime_stt.py
import torch
from stt.vad import VoiceActivityDetector
from stt.chunker import AudioChunker
from stt.whisper_engine import WhisperEngine
from stt.audio_source import wav_frames
from utils.text import SaveText

def main():
    vad = VoiceActivityDetector()
    chunker = AudioChunker(
        min_speech_ms=200,
        min_silence_ms=300
    )
    text_saver = SaveText("transcriptions.txt")

    whisper_engine = WhisperEngine("small")

    for frame_np in wav_frames("tests/test_audio/test_polish.wav"):
        frame = torch.from_numpy(frame_np).float()

        is_speech = vad.is_speech(frame_np)
        #print("speech:", is_speech)
        chunk = chunker.process(frame_np, is_speech)

        if chunk is not None:
            text = whisper_engine.transcribe(chunk)
            if text:
                print("🗣️", text)
                text_saver.save(text)
if __name__ == "__main__":
    main()
