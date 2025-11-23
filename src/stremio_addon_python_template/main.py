import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from nicegui import ui

from stremio_addon_python_template import settings, logger, __version__

# Stremio Addon Manifest - defines addon capabilities
MANIFEST = {
    "id": settings.ADDON_ID,
    "version": __version__,
    "name": "Stremio Python Addon Template",
    "description": "A sample addon built with Python, FastAPI and UV with Pydantic Settings",
    "logo": "https://dl.strem.io/addon-logo.png",
    "resources": ["stream", "catalog"],
    "types": ["movie", "series"],
    "catalogs": [
        {"type": "movie", "id": "python_movies", "name": "Stremio Python Addon Template Catalog"}
    ],
    "idPrefixes": ["tt"],
}

app = FastAPI(title="Stremio Python Addon Template", version=__version__)

# CORS Middleware - required for Stremio web players
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", include_in_schema=False)
async def root():
    """Root endpoint: Redirects to the configuration page."""
    logger.info("Redirecting to configure page.")
    return RedirectResponse(url="/configure")


# NiceGUI Configuration Page (we use here ui.page instead of @app.get)
@ui.page("/configure")
def configure_page(request: Request):
    """Configuration page with NiceGUI interface."""
    logger.info("Configure page accessed.")

    # Get the current host from the request to generate the correct manifest URL
    base_url = str(request.url).replace("/configure", "")
    manifest_url = f"{base_url}/manifest.json"

    with ui.card().classes("w-full max-w-md mx-auto mt-10 p-6"):
        ui.label("Stremio Addon Configuration").classes("text-2xl font-bold mb-4")
        ui.label("Configure your addon settings below:").classes("text-gray-600 mb-4")

        api_key_input = ui.input(
            label="API Key",
            placeholder="Enter your API key here",
            password=True,
            password_toggle_button=True,
        ).classes("w-full mb-4")

        addon_name_input = ui.input(
            label="Addon Name", placeholder="My Custom Addon", value="Python UV Template"
        ).classes("w-full mb-4")

        def save_config():
            logger.info(f"Configuration saved: Addon Name={addon_name_input.value}")
            ui.notify("Configuration saved successfully!", type="positive")

        with ui.row().classes("w-full gap-2"):
            ui.button("Save Configuration", on_click=save_config).props("color=primary")
            ui.link("View Manifest", "/manifest.json", new_tab=True).classes(
                "q-btn q-btn-item non-selectable no-outline q-btn--flat q-btn--rectangle bg-secondary text-white q-btn--actionable q-focusable q-hoverable"
            )

        ui.separator().classes("my-4")

        ui.label("Installation").classes("text-lg font-semibold mb-2")
        ui.label("Copy this URL and add it to Stremio:").classes("text-sm text-gray-600 mb-2")
        ui.code(manifest_url).classes("w-full")


@app.get("/manifest.json")
async def get_manifest():
    """Returns the addon capabilities."""
    logger.info("Manifest requested.")
    return MANIFEST


@app.get("/catalog/{type}/{id}.json")
async def get_catalog(type: str, id: str):
    """Returns catalog items displayed on the Stremio Board."""
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
    """Returns stream links for a specific video."""
    logger.info(f"Stream request: Type={type}, ID={id}")

    streams = []

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
    return {"streams": streams}


# Initialize NiceGUI with FastAPI (must be after all routes are defined)
ui.run_with(app, storage_secret="stremio-addon-secret-key")


# Entry Point
if __name__ == "__main__":
    logger.info(f"Starting server with ADDON_ID: {settings.ADDON_ID}")
    logger.info(f"Addon version is {__version__}")
    logger.info(f"Addon running on http://127.0.0.1:{settings.PORT}")
    logger.info(f"Install URL: http://127.0.0.1:{settings.PORT}/manifest.json")
    uvicorn.run(
        "stremio_addon_python_template.main:app", host="0.0.0.0", port=settings.PORT, reload=True
    )
