<div align="center">

<img src="https://www.google.com/search?q=https://placehold.co/200x80/000000/FFFFFF%3Ftext%3DPYTHON%2BADDON" alt="Addon Logo Placeholder" />

<h1>Stremio Python Addon Template</h1>

<p>This project is a high-performance, asynchronous template for creating Stremio Addons.</p>
<p>Check my <a href="https://github.com/AmineDjeghri/generative-ai-project-template">Generative AI Project Template</a></p>

<img src="https://raw.githubusercontent.com/catppuccin/catppuccin/main/assets/palette/macchiato.png" width="400" />
</div>

<div align="center">

[![python](https://img.shields.io/badge/python-3.11+-blue?logo=python)](https://www.python.org/downloads/release/python-3110/)
[![Debian](https://img.shields.io/badge/Debian-A81D33?logo=debian&logoColor=fff)](https://www.debian.org/)
[![macOS](https://img.shields.io/badge/macOS-000000?logo=apple&logoColor=F0F0F0)](#)

[![Style: Ruff](https://img.shields.io/badge/style-ruff-41B5BE?style=flat)](https://github.com/charliermarsh/ruff)
[![MkDocs](https://img.shields.io/badge/MkDocs-526CFE?logo=materialformkdocs&logoColor=fff)](#)
[![mkdocs-material](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/juftin/mkdocs-material/66d65cf/src/templates/assets/images/badge.json)]()
[![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff)](#)
[![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions&logoColor=white)](#)


</div>

<!-- TOC -->
  * [About The Project](#about-the-project)
  * [👥  Authors](#-authors)
  * [🧠 Features](#-features)
  * [1. Getting started](#1-getting-started)
    * [1.1.  Local Prerequisites](#11-local-prerequisites)
* [This runs: uv sync](#this-runs-uv-sync)
      * [Check the documentation](#check-the-documentation)
    * [1.3 ⚙️ Steps for Installation (Contributors and maintainers)](#13--steps-for-installation-contributors-and-maintainers)
  * [2. Contributing](#2-contributing)
<!-- TOC -->


## About The Project

There are many Stremio addon templates, but most are focused on Node.js. This template brings the power of Python and FastAPI to the ecosystem, prioritizing speed and reliability.

This project is structured as an application (not a reusable library package), designed to run as a web service implementing the Stremio Addon Protocol.

It contains the following key components:

The Stremio Addon (src/stremio_addon): Contains the FastAPI server logic for handling Stremio protocol requests (/manifest.json, /stream/{...}.json, etc.).

Tests (tests): Unit tests for API endpoints using pytest.


## 👥  Authors
- (Author) Amine Djeghri

## 🧠 Features

**Engineering tools:**

- [x] Use UV to manage packages
- [x] pre-commit hooks: use ``ruff`` to ensure the code quality & ``detect-secrets`` to scan the secrets in the code.
- [x] Logging using loguru (with colors)
- [x] Pytest for unit tests
- [x] Dockerized project (Dockerfile) both for development and production
- [x] Make commands to handle everything for you: install, run, test

**CI/CD & Maintenance tools:**

- [x] CI/CD pipelines: ``.github/workflows`` for GitHub
- [x] Local CI/CD pipelines: GitHub Actions using ``github act``
- [x] GitHub Actions for deploying to GitHub Pages with mkdocs gh-deploy
- [x] Dependabot for automatic dependency and security updates

**Documentation tools:**

- [x] Wiki creation and setup of documentation website using Mkdocs
- [x] GitHub Actions for deploying to GitHub Pages with mkdocs gh-deploy

## 1. Getting started

The following files are used in the contribution pipeline:

- ``.env.example``: example of the .env file.
- ``.env`` : contains the environment variables used by the app.
- ``Makefile``: contains the commands to run the app locally.
- ``Dockerfile``: the dockerfile used to build the project inside a container. It uses the Makefile commands to run the app.
- ``.pre-commit-config.yaml``: pre-commit hooks configuration file
- ``pyproject.toml``: contains the pytest, ruff & other configurations.
- ``src/env_settings.py``: logger using logguru and settings  using pydantic.
  the frontend.
- `.github/workflows/**.yml`: GitHub actions configuration files.
- ``.github/dependabot.yml``: dependabot configuration file.
- ``.gitignore``: contains the files to ignore in the project.

### 1.1.  Local Prerequisites
- Python 3.11


git clone the repo
cd stremio-addon-python-template

Install dependencies:

make install
# This runs: uv sync


Usage

Start the server (Development)

``make run``


OR manually: uv run uvicorn stremio_addon.main:app --reload --port 7000


Install in Stremio

Copy the URL from the terminal (e.g., http://127.0.0.1:7000/manifest.json).

Open Stremio, paste the URL into the search bar, and press Enter to install the addon.

#### Check the documentation

You can check the documentation (website), or the ``notebook.ipynb``.

### 1.3 ⚙️ Steps for Installation (Contributors and maintainers)
Check the [CONTRIBUTING.md](CONTRIBUTING.md) file for installation instructions

## 2. Contributing
Check the [CONTRIBUTING.md](CONTRIBUTING.md) file for more information.
