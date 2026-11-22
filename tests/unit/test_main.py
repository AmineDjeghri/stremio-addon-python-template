"""Check the addon routes Stremio calls."""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Import the app away from local .env settings."""
    monkeypatch.chdir(tmp_path)
    from stremio_addon_python_template.main import app

    return TestClient(app)


def test_root_shows_manifest_url(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "http://testserver/manifest.json" in response.text


def test_manifest(client):
    from stremio_addon_python_template.main import MANIFEST

    response = client.get("/manifest.json", headers={"Origin": "https://web.stremio.com"})
    assert response.status_code == 200
    assert response.json() == MANIFEST
    assert response.headers["access-control-allow-origin"] == "*"


def test_catalog(client):
    response = client.get("/catalog/movie/python_movies.json")
    assert response.status_code == 200
    assert [meta["name"] for meta in response.json()["metas"]] == ["Batman", "Big Buck Bunny"]


def test_unknown_catalog_is_empty(client):
    response = client.get("/catalog/movie/unknown.json")
    assert response.json() == {"metas": []}


def test_stream(client):
    response = client.get("/stream/movie/tt1254207.json")
    assert response.status_code == 200
    assert [stream["title"] for stream in response.json()["streams"]] == ["4K [Python Stream]"]


def test_unknown_stream_is_empty(client):
    response = client.get("/stream/movie/tt0000000.json")
    assert response.json() == {"streams": []}
