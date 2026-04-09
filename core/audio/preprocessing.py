import numpy as np
import librosa
from scipy import signal

DISCORD_SAMPLE_RATE = 48000
WHISPER_SAMPLE_RATE = 16000


# ---------------------------------------------------------------------------
# Filters
# ---------------------------------------------------------------------------

def apply_pre_emphasis(audio: np.ndarray, coeff: float = 0.97) -> np.ndarray:
    """Optional pre-emphasis filter."""
    return np.append(audio[0], audio[1:] - coeff * audio[:-1]).astype(np.float32)


def bandpass_filter(
    audio: np.ndarray,
    sample_rate: int,
    low: float = 80.0,
    high: float = 7900.0,
) -> np.ndarray:
    """Keep only speech-relevant frequencies."""
    sos = signal.butter(
        10,
        [low, high],
        btype="bandpass",
        fs=sample_rate,
        output="sos",
    )
    return signal.sosfilt(sos, audio).astype(np.float32)


# ---------------------------------------------------------------------------
# Noise Reduction (improved)
# ---------------------------------------------------------------------------

def reduce_noise(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    n_fft: int = 512,
    over_subtraction: float = 1.5,
    spectral_floor: float = 0.02,
) -> np.ndarray:
    """
    Spectral subtraction with adaptive noise estimation
    (uses lowest-energy frames instead of assuming silence at start).
    """
    hop_length = n_fft // 2

    _, _, Zxx = signal.stft(
        audio,
        fs=sample_rate,
        nperseg=n_fft,
        noverlap=n_fft - hop_length,
    )

    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    # --- estimate noise from lowest-energy frames ---
    frame_energy = np.mean(magnitude, axis=0)
    noise_frames = np.argsort(frame_energy)[: max(1, len(frame_energy) // 10)]
    noise_profile = np.mean(magnitude[:, noise_frames], axis=1, keepdims=True)

    # --- subtraction ---
    magnitude_clean = np.maximum(
        magnitude - over_subtraction * noise_profile,
        spectral_floor * magnitude,
    )

    _, audio_clean = signal.istft(
        magnitude_clean * np.exp(1j * phase),
        fs=sample_rate,
        nperseg=n_fft,
        noverlap=n_fft - hop_length,
    )

    return audio_clean[: len(audio)].astype(np.float32)


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def normalize_amplitude(
    audio: np.ndarray,
    target_rms: float = 0.1,
    min_rms: float = 1e-6,
) -> np.ndarray:
    rms = np.sqrt(np.mean(audio**2))
    if rms < min_rms:
        return audio
    return (audio * (target_rms / rms)).astype(np.float32)


def trim_silence(
    audio: np.ndarray,
    threshold_db: float = 40.0,
    frame_length: int = 2048,
    hop_length: int = 512,
) -> np.ndarray:
    trimmed, _ = librosa.effects.trim(
        audio,
        top_db=threshold_db,
        frame_length=frame_length,
        hop_length=hop_length,
    )
    return trimmed.astype(np.float32)


def resample(
    audio: np.ndarray,
    original_rate: int,
    target_rate: int,
) -> np.ndarray:
    if original_rate == target_rate:
        return audio
    return librosa.resample(audio, orig_sr=original_rate, target_sr=target_rate).astype(
        np.float32
    )


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def preprocess_audio(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    target_sample_rate: int = WHISPER_SAMPLE_RATE,
    use_pre_emphasis: bool = False,
) -> np.ndarray:
    """
    Improved preprocessing pipeline for STT.

    Order:
        1. Trim silence
        2. Band-pass filter
        3. Noise reduction
        4. Normalize
        5. (Optional) Pre-emphasis
        6. Resample
    """

    if len(audio) == 0:
        return audio

    audio = trim_silence(audio)
    audio = bandpass_filter(audio, sample_rate)
    audio = reduce_noise(audio, sample_rate)
    audio = normalize_amplitude(audio)

    if use_pre_emphasis:
        audio = apply_pre_emphasis(audio)

    audio = resample(audio, sample_rate, target_sample_rate)

    return audio