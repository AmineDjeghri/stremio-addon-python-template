# Docker targets
# This file contains the targets to build and run the addon image

.PHONY: docker-build docker-prod

CONTAINER_NAME = stremio-addon-python-template
PORT ?= 7000

docker-build: ## Build the production Docker image
	@printf '%b\n' "${CYAN}Building docker image...${NC}" >&2
	@docker build -t $(CONTAINER_NAME) --progress=plain .
	@printf '%b\n' "${GREEN}docker-build complete${NC}" >&2

docker-prod: docker-build ## Run the addon in Docker on PORT (default 7000)
	@printf '%b\n' "${CYAN}Running the addon on port $(PORT)...${NC}" >&2
	@docker run -it --rm --name $(CONTAINER_NAME) -p $(PORT):7000 $(CONTAINER_NAME)
