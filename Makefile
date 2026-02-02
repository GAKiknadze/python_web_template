.PHONY: help install dev test lint format clean run docker-build docker-up docker-down migrate db-upgrade db-downgrade db-revision docs pre-commit ci performance security release

# Default target
.DEFAULT_GOAL := help

# Colors for output
CYAN := \033[0;36m
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)Available commands:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-20s$(NC) %s\n", $$1, $$2}'

# Installation
install: ## Install production dependencies
	@echo "$(CYAN)Installing production dependencies...$(NC)"
	uv sync --no-dev

dev: ## Install all dependencies including dev and test
	@echo "$(CYAN)Installing all dependencies...$(NC)"
	uv sync --group dev --group test

# Testing
test: ## Run tests
	@echo "$(CYAN)Running tests...$(NC)"
	uv run pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "$(CYAN)Running tests with coverage...$(NC)"
	uv add --dev pytest-cov
	uv run pytest tests/ --cov=src --cov-report=term --cov-report=html --cov-report=xml

test-watch: ## Run tests in watch mode
	@echo "$(CYAN)Running tests in watch mode...$(NC)"
	uv add --dev pytest-watch
	uv run ptw tests/ -- -v

# Linting and Formatting
lint: ## Run linter (Ruff)
	@echo "$(CYAN)Running linter...$(NC)"
	uv run ruff check .

lint-fix: ## Run linter with auto-fix
	@echo "$(CYAN)Running linter with auto-fix...$(NC)"
	uv run ruff check . --fix

format: ## Format code with Ruff
	@echo "$(CYAN)Formatting code...$(NC)"
	uv run ruff format .

format-check: ## Check code formatting
	@echo "$(CYAN)Checking code formatting...$(NC)"
	uv run ruff format --check .

# Pre-commit
pre-commit: ## Run pre-commit hooks on all files
	@echo "$(CYAN)Running pre-commit hooks...$(NC)"
	uv run pre-commit run --all-files

pre-commit-install: ## Install pre-commit hooks
	@echo "$(CYAN)Installing pre-commit hooks...$(NC)"
	uv run pre-commit install

pre-commit-update: ## Update pre-commit hooks
	@echo "$(CYAN)Updating pre-commit hooks...$(NC)"
	uv run pre-commit autoupdate

# Running
run: ## Run the application
	@echo "$(CYAN)Starting application...$(NC)"
	uv run uvicorn main:app --reload --host 0.0.0.0 --port 8000

run-prod: ## Run the application in production mode
	@echo "$(CYAN)Starting application in production mode...$(NC)"
	uv run uvicorn main:app --host 0.0.0.0 --port 8000

# Database
migrate: ## Run database migrations (alias for db-upgrade)
	@$(MAKE) db-upgrade

db-upgrade: ## Upgrade database to latest version
	@echo "$(CYAN)Upgrading database...$(NC)"
	uv run alembic upgrade head

db-downgrade: ## Downgrade database by one revision
	@echo "$(YELLOW)Downgrading database...$(NC)"
	uv run alembic downgrade -1

db-revision: ## Create a new migration revision
	@echo "$(CYAN)Creating new migration...$(NC)"
	@read -p "Enter migration message: " msg; \
	uv run alembic revision --autogenerate -m "$$msg"

db-history: ## Show migration history
	@echo "$(CYAN)Migration history:$(NC)"
	uv run alembic history

db-current: ## Show current database version
	@echo "$(CYAN)Current database version:$(NC)"
	uv run alembic current

db-reset: ## Reset database (downgrade to base and upgrade to head)
	@echo "$(RED)Resetting database...$(NC)"
	uv run alembic downgrade base
	uv run alembic upgrade head

# Docker
docker-build: ## Build Docker image
	@echo "$(CYAN)Building Docker image...$(NC)"
	docker build -t python-web-template:latest .

docker-build-dev: ## Build Docker image for development
	@echo "$(CYAN)Building development Docker image...$(NC)"
	docker build --target development -t python-web-template:dev .

docker-up: ## Start all services with docker-compose
	@echo "$(CYAN)Starting Docker services...$(NC)"
	docker-compose up -d

docker-up-build: ## Build and start all services
	@echo "$(CYAN)Building and starting Docker services...$(NC)"
	docker-compose up -d --build

docker-down: ## Stop all services
	@echo "$(CYAN)Stopping Docker services...$(NC)"
	docker-compose down

docker-logs: ## Show logs from all services
	docker-compose logs -f

docker-ps: ## Show running containers
	docker-compose ps

docker-shell: ## Open shell in app container
	docker-compose exec app /bin/sh

docker-clean: ## Remove all containers, volumes and images
	@echo "$(RED)Cleaning Docker resources...$(NC)"
	docker-compose down -v --rmi all

# CI/CD
ci: lint format-check test ## Run CI checks locally
	@echo "$(GREEN)All CI checks passed!$(NC)"

ci-full: lint format-check test-cov pre-commit ## Run full CI checks
	@echo "$(GREEN)All CI checks passed!$(NC)"

# Performance
performance: ## Run performance tests
	@echo "$(CYAN)Running performance tests...$(NC)"
	uv add --dev locust
	uv run locust --host=http://localhost:8000 --users=100 --spawn-rate=10 --run-time=60s --headless

benchmark: ## Run benchmarks
	@echo "$(CYAN)Running benchmarks...$(NC)"
	uv add --dev pytest-benchmark
	uv run pytest tests/benchmarks/ --benchmark-only

# Security
security: ## Run security checks
	@echo "$(CYAN)Running security checks...$(NC)"
	uv run ruff check . --select S

security-audit: ## Audit dependencies for vulnerabilities
	@echo "$(CYAN)Auditing dependencies...$(NC)"
	uv tool install safety
	uv export --no-hashes > requirements.txt
	uv tool run safety check --file requirements.txt
	rm requirements.txt

# Documentation
docs: ## Generate documentation
	@echo "$(CYAN)Generating documentation...$(NC)"
	@echo "Documentation command to be implemented"

docs-serve: ## Serve documentation locally
	@echo "$(CYAN)Serving documentation...$(NC)"
	@echo "Documentation serve command to be implemented"

# Release
version: ## Show current version
	@echo "$(CYAN)Current version:$(NC)"
	@grep version pyproject.toml | head -1 | awk '{print $$3}' | tr -d '"'

release-patch: ## Create a patch release (0.0.X)
	@echo "$(CYAN)Creating patch release...$(NC)"
	@read -p "Enter release message: " msg; \
	./scripts/release.sh patch "$$msg"

release-minor: ## Create a minor release (0.X.0)
	@echo "$(CYAN)Creating minor release...$(NC)"
	@read -p "Enter release message: " msg; \
	./scripts/release.sh minor "$$msg"

release-major: ## Create a major release (X.0.0)
	@echo "$(CYAN)Creating major release...$(NC)"
	@read -p "Enter release message: " msg; \
	./scripts/release.sh major "$$msg"

# Cleanup
clean: ## Clean up cache and temporary files
	@echo "$(CYAN)Cleaning up...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".ruff_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.coverage" -delete
	rm -rf htmlcov/ .coverage coverage.xml
	rm -rf dist/ build/
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-all: clean docker-clean ## Clean everything including Docker resources
	@echo "$(GREEN)Full cleanup complete!$(NC)"

# Development workflow
setup: dev pre-commit-install db-upgrade ## Complete development setup
	@echo "$(GREEN)Development environment setup complete!$(NC)"
	@echo "$(CYAN)Run 'make run' to start the application$(NC)"

check: lint format-check test ## Quick check before commit
	@echo "$(GREEN)All checks passed!$(NC)"

# Health check
health: ## Check if application is healthy
	@curl -f http://localhost:8000/health || echo "$(RED)Application is not healthy$(NC)"

# Info
info: ## Show project information
	@echo "$(CYAN)Project Information:$(NC)"
	@echo "  Name:    $(GREEN)python-web-template$(NC)"
	@echo "  Python:  $(GREEN)$$(python --version 2>&1)$(NC)"
	@echo "  UV:      $(GREEN)$$(uv --version 2>&1)$(NC)"
	@echo "  Docker:  $(GREEN)$$(docker --version 2>&1)$(NC)"
