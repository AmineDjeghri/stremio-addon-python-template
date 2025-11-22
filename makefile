# Variables
PACKAGE_NAME = src
TEST_DIR = tests

.PHONY: all help install run test lint format clean

all: help

help: ## Show this help message
	@echo "Usage: make [target]"
	@echo ""
	@echo "Targets:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies using uv
	@echo "Installing dependencies..."
	uv sync

run: ## Run the Stremio Addon (Dev Mode)
	@echo "Starting server..."
	uv run src/stremio_addon_python_template/main.py

test: ## Run tests with pytest
	@echo "Running tests..."
	uv run pytest -v

lint: ## Lint code with Ruff
	@echo "Linting code..."
	uv run ruff check .

format: ## Format code with Ruff
	@echo "Formatting code..."
	uv run ruff format .

clean: ## Clean up cache and temp files
	@echo "Cleaning up..."
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +
