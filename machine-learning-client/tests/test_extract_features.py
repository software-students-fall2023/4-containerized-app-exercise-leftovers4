import os
import pytest
import numpy as np
import feature_extraction


def test_feature_array_shape():
    """Test if the feature array has the correct shape."""
    expected_length = 15000 + 40 + 128 + 7 + 1 + 1
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(current_dir, "sample.wav")
    with open(audio_file, "rb") as file:
        audio_info = file.read()
    features = feature_extraction.extract_features(audio_info)
    assert features.shape == (expected_length,)


def test_feature_array_content():
    """Test if the feature array contains valid content."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(current_dir, "sample.wav")
    with open(audio_file, "rb") as file:
        audio_info = file.read()
    features = feature_extraction.extract_features(audio_info)
    assert not np.all(features == 0)
    assert not np.any(np.isnan(features))


def test_invalid_file():
    """Test the function's response to a non-audio file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    invalid_file = os.path.join(current_dir, "sample.txt")
    with pytest.raises(TypeError):
        feature_extraction.extract_features(invalid_file)
