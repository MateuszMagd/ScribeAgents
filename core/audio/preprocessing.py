"""
Audio preprocessing pipeline for speech recognition.

Expected input: float32 numpy array, mono, values in [-1.0, 1.0].
Default sample rate: 48 000 Hz (Discord PCM standard).
"""

import numpy as np
import librosa
from scipy import signal

DISCORD_SAMPLE_RATE = 48_000
WHISPER_SAMPLE_RATE = 16_000


# ---------------------------------------------------------------------------
# Individual preprocessing steps
# ---------------------------------------------------------------------------

def apply_pre_emphasis(audio: np.ndarray, coeff: float = 0.97) -> np.ndarray:
    """Apply a pre-emphasis FIR filter to boost high-frequency content.

    Pre-emphasis compensates for the natural roll-off of the human voice and
    improves the signal-to-noise ratio in higher frequency bands, which helps
    speech recognition models.

    Args:
        audio:  Mono float32 audio signal.
        coeff:  Pre-emphasis coefficient (typically 0.95–0.99).

    Returns:
        Filtered audio as float32 array.
    """
    emphasized = np.append(audio[0], audio[1:] - coeff * audio[:-1])
    return emphasized.astype(np.float32)


def reduce_noise(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    noise_estimation_duration: float = 0.15,
    over_subtraction: float = 2.0,
    spectral_floor: float = 0.02,
) -> np.ndarray:
    """Reduce background noise via spectral subtraction.

    The algorithm estimates a noise magnitude profile from a short segment at
    the beginning of the signal (assumed to be mostly background noise), then
    subtracts that profile from every STFT frame.

    Args:
        audio:                      Mono float32 signal.
        sample_rate:                Sample rate in Hz.
        noise_estimation_duration:  Seconds of audio used for noise profiling.
        over_subtraction:           Multiplier applied to the noise estimate
                                    (values > 1 are more aggressive).
        spectral_floor:             Minimum ratio of the original magnitude
                                    kept after subtraction (prevents musical
                                    noise artefacts).

    Returns:
        Denoised float32 audio array of the same length as *audio*.
    """
    n_fft = 512
    hop_length = n_fft // 2

    # --- noise profile ---
    noise_samples = max(1, int(noise_estimation_duration * sample_rate))
    noise_segment = audio[:noise_samples]

    _, _, Zxx_noise = signal.stft(
        noise_segment, fs=sample_rate, nperseg=n_fft, noverlap=n_fft - hop_length
    )
    noise_profile = np.mean(np.abs(Zxx_noise), axis=-1, keepdims=True)

    # --- full-signal STFT ---
    _, _, Zxx = signal.stft(
        audio, fs=sample_rate, nperseg=n_fft, noverlap=n_fft - hop_length
    )

    # --- spectral subtraction ---
    magnitude = np.abs(Zxx)
    phase = np.angle(Zxx)

    magnitude_clean = np.maximum(
        magnitude - over_subtraction * noise_profile,
        spectral_floor * magnitude,
    )

    # --- reconstruct waveform ---
    _, audio_clean = signal.istft(
        magnitude_clean * np.exp(1j * phase),
        fs=sample_rate,
        nperseg=n_fft,
        noverlap=n_fft - hop_length,
    )

    # istft may pad; trim to the original length
    audio_clean = audio_clean[: len(audio)]
    return audio_clean.astype(np.float32)


def normalize_amplitude(
    audio: np.ndarray,
    target_rms: float = 0.1,
    min_rms: float = 1e-6,
) -> np.ndarray:
    """Normalize audio to a fixed RMS level.

    RMS normalization keeps the perceived loudness consistent across different
    speakers and recording conditions without clipping the signal.

    Args:
        audio:      Mono float32 signal.
        target_rms: Desired RMS energy (0.1 ≈ −20 dBFS).
        min_rms:    Threshold below which the signal is considered silent and
                    returned unchanged.

    Returns:
        Amplitude-normalized float32 array.
    """
    rms = np.sqrt(np.mean(audio ** 2))
    if rms < min_rms:
        return audio
    return (audio * (target_rms / rms)).astype(np.float32)


def trim_silence(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    threshold_db: float = -40.0,
    frame_length: int = 2048,
    hop_length: int = 512,
) -> np.ndarray:
    """Trim leading and trailing silence from an audio signal.

    Uses librosa's energy-based trimming. Frames whose energy is below
    *threshold_db* relative to the peak are removed from both ends.

    Args:
        audio:          Mono float32 signal.
        sample_rate:    Sample rate in Hz (used only as metadata by librosa).
        threshold_db:   dB threshold below peak energy; louder = more aggressive.
        frame_length:   STFT frame size used for energy estimation.
        hop_length:     STFT hop size used for energy estimation.

    Returns:
        Trimmed float32 array (may be the original array if nothing was cut).
    """
    trimmed, _ = librosa.effects.trim(
        audio,
        top_db=-threshold_db,
        frame_length=frame_length,
        hop_length=hop_length,
    )
    return trimmed.astype(np.float32)


def resample(
    audio: np.ndarray,
    original_rate: int = DISCORD_SAMPLE_RATE,
    target_rate: int = WHISPER_SAMPLE_RATE,
) -> np.ndarray:
    """Resample audio to a different sample rate.

    Whisper (and most STT models) expect 16 000 Hz, while Discord delivers
    48 000 Hz PCM. Use this step as the **last** stage of the pipeline so all
    earlier processing runs at the higher, richer sample rate.

    Args:
        audio:          Mono float32 signal.
        original_rate:  Source sample rate in Hz.
        target_rate:    Destination sample rate in Hz.

    Returns:
        Resampled float32 array.
    """
    if original_rate == target_rate:
        return audio
    resampled = librosa.resample(audio, orig_sr=original_rate, target_sr=target_rate)
    return resampled.astype(np.float32)


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def preprocess_audio(
    audio: np.ndarray,
    sample_rate: int = DISCORD_SAMPLE_RATE,
    target_sample_rate: int = WHISPER_SAMPLE_RATE,
) -> np.ndarray:
    """Full preprocessing pipeline for speech-to-text input.

    Steps (in order):
        1. Pre-emphasis   – boost high-frequency speech content.
        2. Noise reduction – spectral subtraction of background noise.
        3. Silence trim   – strip silent edges.
        4. Amplitude norm – bring RMS to a consistent level.
        5. Resample       – convert to the rate expected by the STT model.

    Args:
        audio:              Mono float32 signal in [-1.0, 1.0].
        sample_rate:        Input sample rate in Hz.
        target_sample_rate: Output sample rate in Hz for the STT model.

    Returns:
        Preprocessed float32 audio array ready for transcription.
    """
    if len(audio) == 0:
        return audio

    audio = apply_pre_emphasis(audio)
    audio = reduce_noise(audio, sample_rate)
    audio = trim_silence(audio, sample_rate)
    audio = normalize_amplitude(audio)
    audio = resample(audio, sample_rate, target_sample_rate)

    return audio_
