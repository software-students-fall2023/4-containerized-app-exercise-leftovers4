import pytest
import os
from flask import template_rendered, Flask
from contextlib import contextmanager
from io import BytesIO
import app

from dotenv import load_dotenv

load_dotenv()


@pytest.fixture
def client():
    """a client fixture"""
    os.environ["MONGODB_DATABASE"] = "test_database"
    appl = app.create_app()
    appl.config["TESTING"] = True
    with appl.test_client() as client:
        yield client


@contextmanager
def captured_templates(appl):
    """Template tester"""
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, appl)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, appl)


def test_home_route(client):
    """Tests the home route"""
    with captured_templates(client.application) as templates:
        response = client.get("/home")
        print(response.status_code)
        assert response.status_code == 200
        assert len(templates) == 1
        template, context = templates[0]
        assert template.name == "home.html"
        assert "countdown" in context
        assert context["countdown"] == 10


def test_upload_route_post_method(client):
    """Tests the upload-audio route"""
    data = {"audioFile": (BytesIO(b"my file contents"), "test.wav")}
    response = client.post(
        "/upload-audio", data=data, content_type="multipart/form-data"
    )
    assert response.status_code == 200
