import os
import pytest
import numpy as np
import feature_extraction


def test_feature_array_shape():
    """Test if the feature array has the correct shape."""
    expected_length = 15000 + 40 + 128 + 7 + 1 + 1
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(current_dir, "sample.wav")
    features = feature_extraction.extract_features(audio_file)
    assert features.shape == (expected_length,)


def test_feature_array_content():
    """Test if the feature array contains valid content."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    audio_file = os.path.join(current_dir, "sample.wav")
    features = feature_extraction.extract_features(audio_file)
    assert not np.all(features == 0)
    assert not np.any(np.isnan(features))


def test_invalid_file():
    """Test the function's response to a non-audio file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    invalid_file = os.path.join(current_dir, "sample.txt")
    with pytest.raises(ValueError):
        feature_extraction.extract_features(invalid_file)
