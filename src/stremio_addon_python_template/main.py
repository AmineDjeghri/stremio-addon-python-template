import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from stremio_addon_python_template import settings, logger

# Import the new settings module


# 1. Configuration Logging
# ------------------------


# ----------------
# This tells Stremio what your addon can do. Configuration pulled from settings.
MANIFEST = {
    "id": settings.ADDON_ID,
    "version": "1.0.0",
    "name": "Python UV Template",
    "description": "A sample addon built with Python, FastAPI and UV with Pydantic Settings",
    "logo": "https://dl.strem.io/addon-logo.png",
    "resources": ["stream", "catalog"],
    "types": ["movie", "series"],
    "catalogs": [{"type": "movie", "id": "python_movies", "name": "Python Examples"}],
    "idPrefixes": ["tt"],
}

# Use the app title from Pydantic settings if needed, otherwise keep default
app = FastAPI(title="Stremio Python Addon", version="1.0.0")

# 3. CORS Middleware
# ------------------
# Crucial: Stremio web players run in the browser and need CORS enabled.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 4. Routes
# ---------


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint: Redirects to the manifest."""
    logger.info("Redirecting to manifest.")
    return RedirectResponse(url="/manifest.json")


@app.get("/manifest.json")
async def get_manifest():
    """Returns the addon capabilities."""
    logger.info("Manifest requested.")
    return MANIFEST


@app.get("/catalog/{type}/{id}.json")
async def get_catalog(type: str, id: str):
    """(Optional) Displays a list of items on the Stremio Board."""
    logger.debug(f"Catalog request: Type={type}, ID={id}")
    if type == "movie" and id == "python_movies":
        return {
            "metas": [
                {
                    "id": "tt0096895",  # Batman (1989)
                    "type": "movie",
                    "name": "Batman",
                    "poster": "https://m.media-amazon.com/images/M/MV5BMTYwNjAyODIyMF5BMl5BanBnXkFtZTYwNDMwMDk2._V1_SX300.jpg",
                    "description": "The Dark Knight of Gotham City begins his war on crime.",
                },
                {
                    "id": "tt1254207",  # Big Buck Bunny
                    "type": "movie",
                    "name": "Big Buck Bunny",
                    "poster": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Big_buck_bunny_poster_big.jpg/800px-Big_buck_bunny_poster_big.jpg",
                },
            ]
        }
    return {"metas": []}


@app.get("/stream/{type}/{id}.json")
async def get_stream(type: str, id: str):
    """THE CORE LOGIC: Returns stream links for a specific video."""
    logger.info(f"Stream request: Type={type}, ID={id}")

    streams = []

    # Logic to handle specific movies

    if id == "tt1254207":  # Big Buck Bunny
        streams.append(
            {
                "title": "4K [Python Stream]",
                "url": "http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
            }
        )

    elif id == "tt0096895":  # Batman
        streams.append(
            {
                "title": "1080p [Sample File]",
                "infoHash": "c352d6801679cb6561060988a89458f6728b4377",  # Example InfoHash (Magnet)
                "behaviorHints": {"bingeGroup": "batman-movies"},
            }
        )

    logger.debug(f"Returning {len(streams)} streams.")
    # Always return a dictionary with a "streams" list
    return {"streams": streams}


# 5. Entry Point
# --------------
if __name__ == "__main__":
    logger.info(f"Starting server with ADDON_ID: {settings.ADDON_ID}")
    logger.info(f"Addon running on http://127.0.0.1:{settings.PORT}")
    logger.info(f"Install URL: http://127.0.0.1:{settings.PORT}/manifest.json")
    # We pass the module path to uvicorn, which loads the global 'app' instance.
    # Uvicorn will use the port provided by the command line (via Makefile) or its default (8000).
    # Since we use the Makefile to explicitly pass the PORT, this is clean.
    uvicorn.run(
        "stremio_addon_python_template.main:app", host="0.0.0.0", port=settings.PORT, reload=True
    )
