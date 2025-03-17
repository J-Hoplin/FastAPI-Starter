.PHONY: export-requirements install-dependencies setup docker-build docker-up docker-down help

.DEFAULT_GOAL := help

export-requirements:
	@echo "🚀 Exporting dependencies from uv to requirements.txt"
	@uv pip freeze | grep -v "^-e" > requirements.txt
	@echo "✅ Done."

install-dependencies:
	@echo "✨ Installing dependencies from pyproject.toml"
	@if command -v uv > /dev/null; then \
		uv pip install -e .; \
		echo "✅ Done."; \
	else \
		echo "❌ uv not found. Run 'make setup' first."; \
		exit 1; \
	fi

docker-build:
	@echo "🐳 Building Docker Image"
	@chmod +x ./commands/build.sh
	@./commands/build.sh
	@echo "✅ Done"

docker-up:
	@echo "🚀 Building and starting Docker containers..."
	@if [ ! -f requirements.txt ]; then \
		echo "requirements.txt not found. Generating first..."; \
		$(MAKE) export-requirements; \
	fi
	@docker-compose up -d --build
	@echo "✅ Done"

docker-down:
	@echo "🛑 Stopping Docker containers..."
	@docker-compose down
	@echo "✅ Done"

setup:
	@echo "🔧 Setting up development environment"
	@chmod +x ./commands/setup.sh
	@./commands/setup.sh

help:
	@echo "Commands:"
	@echo "  setup                - Install uv and project dependencies"
	@echo "  export-requirements  - Export dependencies from pyproject.toml to requirements.txt"
	@echo "  install-dependencies - Install dependencies from pyproject.toml"
	@echo "  docker-build         - Build Docker image"
	@echo "  docker-up            - Start Docker containers"
	@echo "  docker-down          - Stop Docker containers"
	@echo "  help                 - Display commands"