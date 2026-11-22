# Run targets
# This file contains targets for running the application

.PHONY: run

run: ## Run the addon server (http://127.0.0.1:7000 by default)
	@printf '%b\n' "${CYAN}Starting the addon server...${NC}" >&2
	@$(UV) run stremio-addon
