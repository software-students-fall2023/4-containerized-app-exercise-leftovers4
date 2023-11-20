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
    elif len(array) < fixed_length:
        return np.pad(array, (0, fixed_length - len(array)), mode = 'constant')
    return array


def extract_features(file_path):
    """
    Extract audio features from the given file path.

    Parameters:
    file_path (str): Path to the audio file.

    Returns:
    numpy.ndarray: Extracted feature array.
    """
    # Check if the file is a .wav or .mp3 file.
    if not file_path.lower().endswith('.wav') and not file_path.lower().endswith('.mp3'):
        raise ValueError(f"The file at {file_path} is not a .wav or .mp3 file.")
    # Exception if audio processing fails.
    try:
        audio, sample_rate = librosa.load(file_path, res_type='kaiser_fast')
    except Exception as e:
        raise ValueError(f"Error processing audio file at {file_path}: {e}") from e

    fixed_length = 7500
    audio, sample_rate = librosa.load(file_path, res_type = 'kaiser_fast')

    mfccs = librosa.feature.mfcc(y = audio, sr = sample_rate, n_mfcc = 40)
    mfccs_processed = np.mean(mfccs.T, axis = 0)

    chroma = librosa.feature.chroma_stft(y = audio, sr = sample_rate).T
    chroma_processed = standardize_array(np.mean(chroma.T, axis = 0),
                                        fixed_length)

    mel = librosa.feature.melspectrogram(y = audio, sr = sample_rate)
    mel_processed = np.mean(mel.T,axis = 0)

    spectral_contrast = librosa.feature.spectral_contrast(y = audio,
                                                        sr = sample_rate)
    spectral_contrast_processed = np.mean(spectral_contrast.T, axis = 0)

    tonnetz = librosa.feature.tonnetz(y = audio, sr = sample_rate).T
    tonnetz_processed = standardize_array(np.mean(tonnetz.T, axis = 0),
                                        fixed_length)

    tempo, _ = librosa.beat.beat_track(y = audio, sr = sample_rate)
    tempo_feature = np.array([tempo])

    song_length = np.array([len(audio) / sample_rate])

    features = np.hstack([mfccs_processed,chroma_processed,mel_processed,
                        spectral_contrast_processed,tonnetz_processed,
                        tempo_feature,song_length])

    return features
