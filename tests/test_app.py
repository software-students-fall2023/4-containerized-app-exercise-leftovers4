"""Testing front end """
# pylint: disable=redefined-outer-name
from unittest.mock import patch
import os
import sys
import pytest
from web_app.app import app

script_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(script_dir)
sys.path.append(project_root)  # adding project root directory to sys.path


@pytest.fixture
def test_client():
    """configuring Flask application to run in testing"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


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
