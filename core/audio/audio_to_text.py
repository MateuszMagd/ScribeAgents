import numpy as np
from faster_whisper import WhisperModel

from core.audio.preprocessing import preprocess_audio, WHISPER_SAMPLE_RATE
from core.audio.postprocessing import postprocess_text
from core.logging.logger import get_logger

_log = get_logger(__name__)
_model: WhisperModel | None = None
_loaded_model_name: str | None = None


def _get_model(model_name: str = "base") -> WhisperModel:
    """Return a cached WhisperModel, loading it on first call."""
    global _model, _loaded_model_name
    if _model is None or _loaded_model_name != model_name:
        _log.info("Loading faster-whisper model: %s", model_name)
        _model = WhisperModel(model_name, device="cpu", compute_type="int8")
        _loaded_model_name = model_name
        _log.info("faster-whisper model '%s' loaded", model_name)
    return _model


def audio_to_text(
    audio: np.ndarray,
    sample_rate: int,
    model_name: str = "base",
    language: str | None = "pl",
) -> str:
    """Convert audio to text using faster-whisper.

    The function preprocesses the raw audio (noise reduction, normalisation,
    resampling to 16 000 Hz) and then runs Whisper transcription.

    Args:
        audio:       Mono float32 signal in [-1.0, 1.0].
        sample_rate: Sample rate of the input signal in Hz.
        model_name:  Whisper model size: "tiny", "base", "small", "medium",
                     "large".  Larger models are more accurate but slower.
        language:    BCP-47 language code (e.g. "pl", "en") or None to let
                     Whisper auto-detect the language.

    Returns:
        Transcribed text string (may be empty for silent input).
    """
    if len(audio) == 0:
        return ""

    audio = preprocess_audio(audio, sample_rate, WHISPER_SAMPLE_RATE)

    if len(audio) == 0:
        return ""

    model = _get_model(model_name)

    segments, _ = model.transcribe(audio, language=language, beam_size=5)
    raw_text = " ".join(segment.text for segment in segments).strip()

    return postprocess_text(raw_text)