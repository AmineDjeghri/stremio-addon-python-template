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


ENV_FILE_PATH := .env
-include $(ENV_FILE_PATH) # keep the '-' to ignore this file if it doesn't exist.(Used in gitlab ci)

# Colors
GREEN=\033[0;32m
YELLOW=\033[0;33m
NC=\033[0m

ifeq ($(OS),Windows_NT)
UV := uv
else
UV := "$$HOME/.local/bin/uv" # keep the quotes incase the path contains spaces
endif


install-uv: ## Install uv
	@echo "${YELLOW}=========> installing uv ${NC}"
ifeq ($(OS),Windows_NT)
	@powershell -NoProfile -ExecutionPolicy Bypass -Command "\
		$errActionPreference = 'Stop'; \
		$uv = Get-Command uv -ErrorAction SilentlyContinue; \
		if ($$uv) { \
		  Write-Host 'uv exists at' $$uv.Source -ForegroundColor Green; \
		  uv self update; \
		} else { \
		  Write-Host 'Installing uv' -ForegroundColor Yellow; \
		  irm https://astral.sh/uv/install.ps1 | iex; \
		}"
else
	@if command -v uv >/dev/null 2>&1; then \
		echo "${GREEN}uv exists at $$(command -v uv) ${NC}"; \
		$(UV) self update; \
	else \
		echo "${YELLOW}Installing uv${NC}"; \
		curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR="$$HOME/.local/bin" sh; \
	fi
endif

install:install-uv ## Install dependencies using uv
	@echo "Installing dependencies..."
	uv sync

run: ## Run the Stremio Addon (Dev Mode)
	@echo "Starting server..."
	uv run src/stremio_addon_python_template/main.py




pre-commit-install:
	@echo "${YELLOW}=========> Installing pre-commit...${NC}"
	$(UV) run pre-commit install

pre-commit:pre-commit-install ## Run pre-commit
	@echo "${YELLOW}=========> Running pre-commit...${NC}"
	$(UV) run pre-commit run --all-files

lint: ## Lint code with Ruff
	@echo "Linting code..."
	uv run ruff check .

format: ## Format code with Ruff
	@echo "Formatting code..."
	uv run ruff format .

####### local CI / CD ########
# uv caching :
prune-uv: ## Prune uv cache
	@echo "${YELLOW}=========> Prune uv cache...${NC}"
	@$(UV) cache prune
# clean uv caching
clean-uv-cache: ## Clean uv cache
	@echo "${YELLOW}=========> Cleaning uv cache...${NC}"
	@$(UV) cache clean



clean: clean-uv-cache ## Clean up cache and temp files
	@echo "Cleaning up..."
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf __pycache__
	find . -type d -name "__pycache__" -exec rm -rf {} +

# Github actions locally
install-act:
	@echo "${YELLOW}=========> Installing github actions act to test locally${NC}"
	curl --proto '=https' --tlsv1.2 -sSf https://raw.githubusercontent.com/nektos/act/master/install.sh | bash
	@echo -e "${YELLOW}Github act version is :"
	@./bin/act --version

act: install-act ## Run Github Actions locally
	@echo "${YELLOW}Running Github Actions locally...${NC}"
	@./bin/act --env-file .env

# clear GitHub local caches
clear_ci_cache: ## Clear GitHub local caches
	@echo "${YELLOW}Clearing CI cache...${NC}"
	@echo "${YELLOW}Clearing Github ACT local cache...${NC}"
	rm -rf ~/.cache/act ~/.cache/actcache


######## Tests ########
######## Tests ########
test-installation:
	@echo "${YELLOW}=========> Testing installation...${NC}"
	@$(UV) run --directory . hello

test: ## Run tests with pytest
	@echo "${YELLOW}Running tests...${NC}"
	@$(UV) run pytest tests


######## Builds ########
# This build the documentation based on current code 'src/' and 'docs/' directories
# This is to run the documentation locally to see how it looks
build-package: ## build package (wheel)
	@echo "${YELLOW}=========> Building python package and wheel...${NC}"
	@$(UV) build

deploy-doc-local: ## Deploy documentation locally
	@echo "${YELLOW}Deploying documentation locally...${NC}"
	@$(UV) run mkdocs build && $(UV) run mkdocs serve

# Deploy it to the gh-pages branch in your GitHub repository (you need to setup the GitHub Pages in github settings to use the gh-pages branch)
deploy-doc-gh: ## Deploy documentation in github actions
	@echo "${YELLOW}Deploying documentation in github actions..${NC}"
	@$(UV) run mkdocs build && $(UV) run mkdocs gh-deploy
