SHELL = /bin/bash
.ONESHELL:
MAKEFLAGS += --no-builtin-rules

# Variables
VENV_DIR = .venv
BLACK = $(VENV_DIR)/bin/black
FLAKE8 = $(VENV_DIR)/bin/flake8
PIP = $(VENV_DIR)/bin/pip
PYTEST = $(VENV_DIR)/bin/pytest
PYTHON = $(VENV_DIR)/bin/python
UVICORN = $(VENV_DIR)/bin/uvicorn

# Help Task
help:
	@printf "Usage: make [target] [VARIABLE=value]\nTargets:\n"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

# Virtual Environment Management
venv: ## Create a virtual environment
	@python -m venv $(VENV_DIR)
	@$(PIP) install --upgrade pip

clean-venv: ## Remove the virtual environment
	@rm -rf $(VENV_DIR)

# Pre-commit Hooks
pre-commit-install: ## Install pre-commit hooks
	@pre-commit install
	@pre-commit gc

pre-commit-uninstall: ## Uninstall pre-commit hooks
	@pre-commit uninstall

validate: ## Validate files with pre-commit hooks
	@pre-commit run --all-files

# Dependency Management
install-deps: venv ## Install Python dependencies
	@echo "Installing Python dependencies"
	@$(PIP) install --requirement requirements.txt

install-dev-deps: install-deps ## Install development dependencies
	@echo "Installing development dependencies"
	@$(PIP) install --requirement requirements-dev.txt

# Linting and Formatting
lint: venv ## Run linters
	@$(FLAKE8) .

format: venv ## Format code with black
	@$(BLACK) .

# Testing
# test: install-dev-deps ## Run application tests
test: venv ## Run application tests
	@echo "Running unit tests"
	@$(PYTEST)

# Running the Application
run: venv ## Run the application
	@$(UVICORN) app.main:app --reload

# Cleaning
clean-pycache: ## Remove Python cache files
	@find . -type d -name "__pycache__" -exec rm -rf {} +

clean: clean-pycache ## Clean project (pycache, coverage, etc.)
	@rm -rf .coverage htmlcov

# Docker Tasks
docker-build: ## Build the Docker image
	@docker build --tag inquire-docs .

docker-run: docker-build ## Run the Docker container
	@docker run --rm --name inquire-docs --publish 8000:8000 inquire-docs

docker-clean: ## Remove dangling Docker images
	@docker rm --force inquire-docs
  @docker rmi --force inquire-docs
