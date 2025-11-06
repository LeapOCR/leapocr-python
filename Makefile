.PHONY: help install test test-unit test-integration lint format build publish clean dev-setup validate

# Variables
PYTHON := python3
UV := uv

# Default target
help: ## Show this help message
	@echo "LeapOCR Python SDK - Development Commands"
	@echo "========================================"
	@echo ""
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-20s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# Development Setup
install: ## Install dependencies with UV
	$(UV) sync

install-dev: ## Install development dependencies
	$(UV) sync --group dev

dev-setup: install-dev ## Complete development setup
	@echo "✅ Development environment setup complete!"
	@echo "📋 Next steps:"
	@echo "  1. Set LEAPOCR_API_KEY environment variable for integration tests"
	@echo "  2. Run tests: make test"
	@echo "  3. Format code: make format"

# Testing
test: ## Run all tests
	$(UV) run pytest

test-unit: ## Run unit tests only
	$(UV) run pytest -m "not integration and not slow"

test-integration: ## Run integration tests only
	$(UV) run pytest -m integration

test-coverage: ## Run tests with coverage
	$(UV) run pytest --cov=leapocr --cov-report=html --cov-report=term

# Code Quality
lint: ## Run linter and type checker
	$(UV) run ruff check src/ tests/ examples/
	$(UV) run mypy src/

format: ## Format code with ruff
	$(UV) run ruff format

# Code Generation
generate: ## Generate Python client from OpenAPI spec
	@echo "🎯 Generating Python SDK from OpenAPI spec..."
	./scripts/generate-sdk.sh

validate-spec: ## Validate OpenAPI spec accessibility
	@echo "🔍 Validating OpenAPI spec accessibility..."
	@curl -f -s http://localhost:8080/api/v1/swagger.json > /dev/null && echo "✅ OpenAPI spec is accessible" || echo "❌ Cannot access OpenAPI spec"

# Building and Publishing
build: ## Build package
	$(UV) build

publish: ## Publish to PyPI
	$(UV) publish

# Examples
examples: ## Run examples (requires API key)
	@echo "🚀 Running examples..."
	@if [ -z "$$LEAPOCR_API_KEY" ]; then \
		echo "❌ LEAPOCR_API_KEY environment variable is required"; \
		exit 1; \
	fi
	$(UV) run python examples/basic.py
	$(UV) run python examples/advanced.py

# Documentation
docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	$(UV) run mkdocs build

# Cleanup
clean: ## Clean build artifacts
	@echo "🧹 Cleaning up..."
	rm -rf build/
	rm -rf dist/
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf .ruff_cache/
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

clean-generated: ## Clean generated files only
	@echo "🧹 Cleaning generated files..."
	rm -rf src/leapocr/gen/
	rm -rf openapi-*.json

# Validation
validate: lint test-unit ## Run all validation checks
	@echo "✅ All validation checks passed!"

# CI/CD
ci-test: lint test-unit ## Run CI tests
	@echo "✅ CI tests passed!"

ci-test-full: validate test ## Run full CI test suite
	@echo "✅ Full CI test suite passed!"

# Development utilities
shell: ## Start development shell with dependencies
	$(UV) shell

upgrade: ## Upgrade dependencies
	$(UV) sync --upgrade

# Pre-commit
pre-commit: ## Install pre-commit hooks
	$(UV) run pre-commit install

check-pre-commit: ## Run pre-commit checks
	$(UV) run pre-commit run --all-files