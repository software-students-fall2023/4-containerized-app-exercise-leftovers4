"""Testing front end """
from unittest.mock import patch, mock_open, MagicMock
import io
import os
import sys
import pytest

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)  # adding project root directory to sys.path

from web_app.app import app


@pytest.fixture
def client():
    """configuring Flask application to run in testing"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_route(client):
    """Tests the index route."""
    response = client.get("/")
    assert response.status_code == 302  # assume redirect
    assert response.location.endswith("/home")  # redirect to home


def test_home_route(client):
    """Tests the home route."""
    response = client.get("/home")
    assert response.status_code == 200


def test_upload_audio_no_file(client):
    """Tests the upload_audio route with no file uploaded."""
    response = client.post("/upload-audio")
    assert response.status_code == 400
    assert b"No audio file found" in response.data


# def test_upload_audio_with_file(client):
#     """Tests the upload_audio route with a file uploaded."""

#     mock_file = mock_open(read_data=b"some wav data")
#     with patch("subprocess.run") as mock_run, patch("os.remove") as mock_remove:
#         mock_run.return_value = MagicMock(returncode=0)

#         # reference to unpatched open
#         original_open = open

#         # side effect for the mock to only apply to specific filenames
#         def open_side_effect(file, *args, **kwargs):
#             # checking if trying to open the file we're interested in mocking
#             # else call original open
#             if file in ["temp_input_file", "temp_output_file.wav"]:
#                 return mock_file()
#             else:
#                 return original_open(file, *args, **kwargs)

#         with patch("builtins.open", side_effect=open_side_effect):
#             data = {
#                 "audioFile": (io.BytesIO(b"some initial audio data"), "test.mp3"),
#             }
#             response = client.post(
#                 "/upload-audio", data=data, content_type="multipart/form-data"
#             )

#     assert response.status_code == 200
#     assert mock_remove.call_count == 2  # remove temp files


def test_upload_audio_with_file(client):
    """Tests the upload_audio route with a file uploaded."""
    # mock pymongo collection methods used in the upload_audio function
    with patch("web_app.app.collection.find") as mock_find, patch(
        "web_app.app.collection.insert_one"
    ) as mock_insert_one:
        mock_find.return_value.sort.return_value.limit.return_value = [MagicMock()]

        mock_insert_one.return_value = None

        data = {
            "audioFile": (io.BytesIO(b"some initial audio data"), "test.mp3"),
        }
        response = client.post(
            "/upload-audio", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200


def test_results_route(client):
    """
    Tests the results route.
    """
    # mock database call
    with patch("web_app.app.collection.find") as mock_find:
        mock_find.return_value.sort.return_value.limit.return_value = [
            {"_id": 1, "name": "Test Audio 1"},
        ]
        # get /results
        response = client.get("/results")

        # OK response
        assert response.status_code == 200
