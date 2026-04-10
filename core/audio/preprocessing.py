import numpy as np
import librosa
from scipy import signal

DISCORD_SAMPLE_RATE = 48000
WHISPER_SAMPLE_RATE = 16000


def apply_pre_emphasis(audio: np.ndarray, coeff: float = 0.97) -> np.ndarray:
    """Apply pre-emphasis filter to boost high frequencies."""
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


def reduce_noise(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    n_fft: int = 512,
    over_subtraction: float = 1.5,
    spectral_floor: float = 0.02,
) -> np.ndarray:
    """Reduce noise via spectral subtraction with adaptive noise estimation."""
    hop_length = n_fft // 2

    _, _, Zxx = signal.stft(
        audio,
        fs=sample_rate,
        nperseg=n_fft,
        noverlap=n_fft - hop_length,
    )

    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    frame_energy = np.mean(magnitude, axis=0)
    noise_frames = np.argsort(frame_energy)[: max(1, len(frame_energy) // 10)]
    noise_profile = np.mean(magnitude[:, noise_frames], axis=1, keepdims=True)

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


def normalize_amplitude(
    audio: np.ndarray,
    target_rms: float = 0.1,
    min_rms: float = 1e-6,
) -> np.ndarray:
    """Normalize audio amplitude to a target RMS level."""
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
    """Trim leading and trailing silence."""
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
    """Resample audio to a different sample rate."""
    if original_rate == target_rate:
        return audio
    return librosa.resample(audio, orig_sr=original_rate, target_sr=target_rate).astype(
        np.float32
    )


def preprocess_audio(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    target_sample_rate: int = WHISPER_SAMPLE_RATE,
    use_pre_emphasis: bool = False,
) -> np.ndarray:
    """Run the full audio preprocessing pipeline: trim, bandpass, denoise, normalize, resample."""
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