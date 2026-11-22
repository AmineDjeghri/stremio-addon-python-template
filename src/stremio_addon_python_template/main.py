"""Stremio addon server: the manifest plus the catalog and stream routes."""

from html import escape
from importlib.metadata import version

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from stremio_addon_python_template.settings import logger, settings

__version__ = version("stremio-addon-python-template")

# Stremio Addon Manifest - defines addon capabilities
MANIFEST = {
    "id": settings.ADDON_ID,
    "version": __version__,
    "name": "Stremio Python Addon Template",
    "description": "A sample addon built with Python, FastAPI and uv",
    "logo": "https://dl.strem.io/addon-logo.png",
    "resources": ["catalog", "stream"],
    "types": ["movie"],
    "catalogs": [
        {"type": "movie", "id": "python_movies", "name": "Stremio Python Addon Template Catalog"}
    ],
    "idPrefixes": ["tt"],
}

# Sample data: replace with your own source.
METAS = {
    "tt0096895": {
        "id": "tt0096895",
        "type": "movie",
        "name": "Batman",
        "poster": "https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_SX300.jpg",
        "description": "The Dark Knight of Gotham City begins his war on crime.",
    },
    "tt1254207": {
        "id": "tt1254207",
        "type": "movie",
        "name": "Big Buck Bunny",
        "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/800px-Big_buck_bunny_poster_big.jpg",
    },
}

STREAMS = {
    "tt1254207": [
        {
            "title": "4K [Python Stream]",
            "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
        }
    ],
    "tt0096895": [
        {
            "title": "1080p [Sample File]",
            "infoHash": "c352d6801679cb6561060988a89458f6728b4377",  # pragma: allowlist secret
            "behaviorHints": {"bingeGroup": "batman-movies"},
        }
    ],
}

app = FastAPI(title="Stremio Python Addon Template", version=__version__)

# CORS - required for Stremio web players
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request) -> str:
    """Show the manifest URL to install the addon."""
    manifest_url = escape(f"{request.base_url}manifest.json")
    return f"<h1>{MANIFEST['name']}</h1><p>Add this URL in Stremio: <code>{manifest_url}</code></p>"


@app.get("/manifest.json")
async def get_manifest() -> dict:
    """Return the addon capabilities."""
    return MANIFEST


@app.get("/catalog/{type}/{id}.json")
async def get_catalog(type: str, id: str) -> dict:
    """Return the items shown in a catalog row."""
    logger.debug(f"Catalog request: type={type}, id={id}")
    if type == "movie" and id == "python_movies":
        return {"metas": list(METAS.values())}
    return {"metas": []}


@app.get("/stream/{type}/{id}.json")
async def get_stream(type: str, id: str) -> dict:
    """Return the playable streams of one item."""
    logger.debug(f"Stream request: type={type}, id={id}")
    return {"streams": STREAMS.get(id, [])}


def run() -> None:
    """Start the addon server (console script `stremio-addon`)."""
    logger.info(f"Install URL: http://{settings.HOST}:{settings.PORT}/manifest.json")
    uvicorn.run(app, host=settings.HOST, port=settings.PORT)


if __name__ == "__main__":
    run()
