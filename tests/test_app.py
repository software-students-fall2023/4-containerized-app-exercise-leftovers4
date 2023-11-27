"""Testing front end """
from unittest.mock import patch, mock_open, MagicMock
from bson import Binary
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


# def test_upload_audio_no_file(client):
#     """Tests the upload_audio route with no file uploaded."""
#     response = client.post("/upload-audio")
#     assert response.status_code == 400
#     assert b"No audio file found" in response.data


def test_upload_audio_with_file(client):
    """Tests the upload_audio route with a file uploaded."""

    mock_file = mock_open(read_data=b"some wav data")

    # mock pymongo collection methods and MongoClient
    mock_collection = MagicMock()
    mock_client = MagicMock()
    mock_client.return_value.get_database.return_value.get_collection.return_value = (
        mock_collection
    )

    original_open = open

    # Patching MongoDB client, subprocess, and os.remove
    with patch("pymongo.MongoClient", mock_client), patch(
        "subprocess.run", MagicMock(returncode=0)
    ), patch("os.remove", MagicMock()), patch(
        "builtins.open", mock_open(read_data=b"some wav data")
    ) as mock_open_obj:

        def open_side_effect(file, mode="r", *args, **kwargs):
            if file in ["temp_input_file", "temp_output_file.wav"] and mode in [
                "rb",
                "wb",
            ]:
                return mock_file()
            else:
                return original_open(file, mode, *args, **kwargs)

        mock_open_obj.side_effect = open_side_effect

        data = {
            "audioFile": (io.BytesIO(b"some initial audio data"), "test.wav"),
        }

        print("in data", data)

        response = client.post(
            "/upload-audio", data=data, content_type="multipart/form-data"
        )

        assert response.status_code == 200

        # mock_collection.insert_one.assert_called_once()
        # mock_collection.insert_one.assert_called()


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
