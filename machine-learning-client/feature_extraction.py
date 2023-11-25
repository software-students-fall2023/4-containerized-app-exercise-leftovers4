"""
This module provides functionality for audio feature extraction and processing,
including the standardization of arrays to a fixed length.
"""
import io
import librosa
import numpy as np


def standardize_array(array, fixed_length):
    """
    Standarizes an array to fixed size using truncating or padding.

    Parameters:
    array (numpy.ndarray): An input array to be standardized in length.
    fixed_length (int): The target fixed length for the array.

    Returns:
    numpy.ndarray: The array adjusted to the specified fixed length.
    """
    if len(array) > fixed_length:
        return array[:fixed_length]
    if len(array) < fixed_length:
        return np.pad(array, (0, fixed_length - len(array)), mode="constant")
    return array


# def extract_features(file_path):
#     """
#     Extract audio features from the given file path.

#     Parameters:
#     file_path (str): Path to the audio file.

#     Returns:
#     numpy.ndarray: Extracted feature array.
#     """
#     # Check if the file is a .wav or .mp3 file.
#     if not file_path.lower().endswith(".wav") and not file_path.lower().endswith(
#         ".mp3"
#     ):
#         raise ValueError(f"The file at {file_path} is not a .wav or .mp3 file.")
#     # Exception if audio processing fails.
#     try:
#         audio, sample_rate = librosa.load(file_path, res_type="kaiser_fast")
#     except Exception as e:
#         raise ValueError(f"Error processing audio file at {file_path}: {e}") from e

#     fixed_length = 7500

#     # Feature extraction
#     mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
#     chroma = standardize_array(
#         np.mean(librosa.feature.chroma_stft(y=audio, sr=sample_rate).T, axis=0),
#         fixed_length,
#     )
#     mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sample_rate).T, axis=0)
#     spectral_contrast = np.mean(
#         librosa.feature.spectral_contrast(y=audio, sr=sample_rate).T, axis=0
#     )
#     tonnetz = standardize_array(
#         np.mean(librosa.feature.tonnetz(y=audio, sr=sample_rate).T, axis=0),
#         fixed_length,
#     )
#     tempo_feature = np.array([librosa.beat.beat_track(y=audio, sr=sample_rate)[0]])
#     song_length = np.array([len(audio) / sample_rate])

#     # Combine all features
#     features = np.hstack(
#         [mfccs, chroma, mel, spectral_contrast, tonnetz, tempo_feature, song_length]
#     )

#     return features


def extract_features(audio_data, sample_rate=44100):
    """
    Extract audio features from an in-memory audio data.

    Parameters:
    audio_data (bytes): Binary audio data.
    sample_rate (int): Sampling rate for audio data.

    Returns:
    numpy.ndarray: Extracted feature array.
    """
    if not isinstance(audio_data, bytes):
        raise TypeError("Invalid input type. Expected binary data.")

    # Load audio data from binary data
    audio, _ = librosa.load(io.BytesIO(audio_data), sr=sample_rate)

    # fixed_length = 7500

    # Feature extraction
    mfccs = np.mean(librosa.feature.mfcc(y=audio, sr=sample_rate, n_mfcc=40).T, axis=0)
    # chroma = standardize_array(
    #     np.mean(librosa.feature.chroma_stft(y=audio, sr=sample_rate).T, axis=0),
    #     fixed_length,
    # )
    mel = np.mean(librosa.feature.melspectrogram(y=audio, sr=sample_rate).T, axis=0)
    spectral_contrast = np.mean(
        librosa.feature.spectral_contrast(y=audio, sr=sample_rate).T, axis=0
    )
    # tonnetz = standardize_array(
    #     np.mean(librosa.feature.tonnetz(y=audio, sr=sample_rate).T, axis=0),
    #     fixed_length,
    # )
    tempo_feature = np.array([librosa.beat.beat_track(y=audio, sr=sample_rate)[0]])
    song_length = np.array([len(audio) / sample_rate])

    # Combine all features
    features = np.hstack(
        [mfccs, mel, spectral_contrast, tempo_feature, song_length]
    )

    return features
