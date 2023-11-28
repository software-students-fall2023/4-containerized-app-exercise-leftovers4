"""Testing front end """
# pylint: disable=redefined-outer-name
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import subprocess
import pytest
from web_app.app import app, convert_to_wav


script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)  # adding project root directory to sys.path


@pytest.fixture
def test_client():
    """configuring Flask application to run in testing"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


@pytest.fixture
def mock_subprocess_run():
    """mokcing subprocess"""
    with patch("subprocess.run") as mock_run:
        yield mock_run


@pytest.fixture
def mock_os_remove():
    """mocking remove"""
    with patch("os.remove") as mock_remove:
        yield mock_remove


def test_index_route(test_client):
    """Tests the index route."""
    response = test_client.get("/")
    assert response.status_code == 302  # assume redirect
    assert response.location.endswith("/home")  # redirect to home


def test_home_route(test_client):
    """Tests the home route."""
    response = test_client.get("/home")
    assert response.status_code == 200


def test_upload_audio_no_file(test_client):
    """Tests the upload_audio route with no file uploaded."""
    response = test_client.post("/upload-audio")
    assert response.status_code == 400
    assert b"No audio file found" in response.data


def test_results_route(test_client):
    """
    Tests the results route.
    """
    # mock database call
    with patch("web_app.app.collection.find") as mock_find:
        mock_find.return_value.sort.return_value.limit.return_value = [
            {"_id": 1, "name": "Test Audio 1"},
        ]
        # get /results
        response = test_client.get("/results")

        # OK response
        assert response.status_code == 200


def test_convert_to_wav_failure(mock_subprocess_run, mock_os_remove):
    """
    Test the convert_to_wav function when the subprocess call fails.
    """

    mock_input_data = b"fake audio data"
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(1, "ffmpeg")

    with patch("builtins.open", mock_open()):
        result = convert_to_wav(mock_input_data)

    assert result is None
    mock_subprocess_run.assert_called_once()
    # files should not be removed if the conversion fails
    mock_os_remove.assert_not_called()


def test_convert_to_wav_success(mock_subprocess_run, mock_os_remove):
    """
    Test the convert_to_wav function when the subprocess call is successful.
    """
    mock_input_data = b"fake audio data"
    mock_wav_data = b"converted wav data"
    m = mock_open(read_data=mock_wav_data)
    mock_subprocess_run.return_value = MagicMock(returncode=0)

    with patch("builtins.open", m):
        result = convert_to_wav(mock_input_data)

    assert result == mock_wav_data
    m.assert_any_call("temp_input_file", "wb")
    m.assert_any_call("temp_output_file.wav", "rb")
    assert m.call_count == 2
    mock_subprocess_run.assert_called_once()
    mock_os_remove.assert_any_call("temp_input_file")
    mock_os_remove.assert_any_call("temp_output_file.wav")
