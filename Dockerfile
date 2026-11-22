# Production image: `make docker-prod` builds it and serves the addon on port 7000.
# PYTHON_VERSION: keep it equal to `requires-python` in pyproject.toml; Renovate proposes both in
# its "python runtime" group.
ARG PYTHON_VERSION=3.14.7
FROM python:${PYTHON_VERSION}-slim

# uv, and make to run the project's make targets
COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /uvx /usr/local/bin/
RUN apt-get update && apt-get install -y --no-install-recommends make ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# The environment lives outside /app
WORKDIR /app
ENV UV_PROJECT_ENVIRONMENT=/opt/venv \
    PATH="/opt/venv/bin:$PATH" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Only what the install needs (.dockerignore keeps everything else, including .env, out)
COPY Makefile pyproject.toml uv.lock README.md ./
COPY makefiles/ makefiles/
COPY src/ src/
RUN make install-prod UV_SYNC_FLAGS="--locked --no-editable"

# Runtime settings (settings.py): listen on every interface inside the container
ENV HOST=0.0.0.0 \
    PORT=7000 \
    LOGGING_LEVEL=INFO

# Run unprivileged: the addon is reachable from the internet
RUN useradd --system --no-create-home app
USER app

EXPOSE 7000
CMD ["stremio-addon"]
