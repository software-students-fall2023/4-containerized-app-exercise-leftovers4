import pytest
import os
import knn_classifier


def test_load_model_success():
    """Test loading a model successfully from a valid file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    valid_model_path = os.path.join(parent_dir, "knn_classifier.pkl")
    model = knn_classifier.load_model(valid_model_path)
    assert model is not None


def test_load_model_invalid_path():
    """Test loading a model from a non-existent file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    invalid_model_path = os.path.join(current_dir, "sample_knn_classifier.wav")
    with pytest.raises(FileNotFoundError):
        knn_classifier.load_model(invalid_model_path)


def test_load_model_invalid_content():
    """Test loading a model from a file that does not contain a valid model."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    invalid_content_path = os.path.join(current_dir, "invalid_classifier.pkl")
    with pytest.raises(Exception):
        knn_classifier.load_model(invalid_content_path)
