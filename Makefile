.PHONY: help install install-dev test test-cov clean run examples format lint

help:
	@echo "Aura IA - Available Commands:"
	@echo ""
	@echo "  make install        Install production dependencies"
	@echo "  make install-dev    Install development dependencies"
	@echo "  make test           Run unit tests"
	@echo "  make test-cov       Run tests with coverage report"
	@echo "  make run            Run the main test script"
	@echo "  make examples       Run usage examples"
	@echo "  make clean          Clean build artifacts and cache"
	@echo "  make lint           Run code linting (if configured)"
	@echo "  make format         Format code (if configured)"
	@echo ""

install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

test:
	pytest tests/ -v

test-cov:
	pytest --cov=src/aura_ia --cov-report=html --cov-report=term tests/

run:
	python main.py

examples:
	python examples.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".coverage" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "htmlcov" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "build" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "dist" -exec rm -rf {} + 2>/dev/null || true
	@echo "Cleaned up build artifacts and cache files"

lint:
	@echo "Linting not configured yet. Install flake8 or pylint if needed."

format:
	@echo "Formatting not configured yet. Install black or autopep8 if needed."
