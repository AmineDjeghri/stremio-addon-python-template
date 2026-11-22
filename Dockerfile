# Production image: `make docker-prod` builds and runs it on port 7000.
# Keep PYTHON_VERSION equal to `requires-python` in pyproject.toml; Renovate proposes both in its
# "python runtime" group.
ARG PYTHON_VERSION=3.14.7
FROM python:${PYTHON_VERSION}-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.6 /uv /bin/uv

ENV PYTHONUNBUFFERED=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    HOST=0.0.0.0 \
    PORT=7000 \
    LOGGING_LEVEL=INFO

WORKDIR /app

# Dependencies first, so code changes reuse this layer.
COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-install-project

COPY README.md ./
COPY src ./src
RUN uv sync --locked

RUN useradd --system --no-create-home app
USER app

EXPOSE 7000
CMD ["/app/.venv/bin/stremio-addon"]
