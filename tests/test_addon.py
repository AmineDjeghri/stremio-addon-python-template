from fastapi.testclient import TestClient

from stremio_addon_python_template.main import MANIFEST, app

client = TestClient(app)


def test_read_root():
    """Test that root redirects to configure page."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/configure"


def test_manifest():
    """Test that manifest returns correct JSON."""
    response = client.get("/manifest.json")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == MANIFEST["id"]
    assert "stream" in data["resources"]


def test_catalog():
    """Test catalog response structure."""
    response = client.get("/catalog/movie/python_movies.json")
    assert response.status_code == 200
    data = response.json()
    assert "metas" in data
    assert len(data["metas"]) > 0
    assert data["metas"][0]["name"] == "Batman"


def test_stream_response():
    """Test stream logic for Big Buck Bunny."""
    response = client.get("/stream/movie/tt1254207.json")
    assert response.status_code == 200
    data = response.json()
    assert "streams" in data
    assert len(data["streams"]) == 1
    assert data["streams"][0]["title"] == "4K [Python Stream]"
