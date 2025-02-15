.PHONY: venv
venv: ## Install the virtual environment
	@echo "🚀 Creating virtual environment using uv"
	@python3.11 -m venv .venv
	@source .venv/bin/activate

.PHONY: install
install: ## Install tools and other dependencies
	@echo "🚀 Creating virtual environment using uv"
	@brew install python@3.11
	@brew install make
	@brew install uv

.PHONY: db-config
db-config: ## Initialize database
	@echo "🚀 Initializing database"
	@brew install postgresql
	@brew services start postgresql
	@createuser -s postgres
	@createdb postgres

.PHONY: db-config-linux
db-config-linux: ## Initialize database on Linux
	@echo "🚀 Initializing database"
	@sudo apt-get update
	@sudo apt-get install postgresql
	@sudo service postgresql start
	@createuser -s postgres
	@createdb postgres


.PHONY: dependencies
dependencies: ## Download dependencies
	@uv sync
	@uv run pre-commit install
	
.PHONY: check
check:
	@echo "🚀 Linting code: Running Ruff lint and format check"
	@ruff check app
	@ruff format app --check

.PHONY: fix
fix: ## Run code quality tools.
	@echo "🚀 Checking lock file consistency with 'pyproject.toml'"
	@uv lock --locked
	@echo "🚀 Linting code: Running pre-commit"
	@uv run pre-commit run -a
##  @echo "🚀 Static type checking: Running mypy"

.PHONY: dep-check
dep-check: ## Dependency Check
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@uv run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@uv run coverage run --source=app -m pytest -v tests
	@uv run coverage report -m

.PHONY: coverage
coverage: test
	@uv run coverage html
	@open htmlcov/index.html

.PHONY: build
build: clean-build ## Build wheel file
	@echo "🚀 Creating wheel file"
	@uvx --from build pyproject-build --installer uv

.PHONY: clean-build
clean-build: ## Clean build artifacts
	@echo "🚀 Removing build artifacts"
	@uv run python -c "import shutil; import os; shutil.rmtree('dist') if os.path.exists('dist') else None"

.PHONY: dev
dev:
	@echo "🚀 Starting dev with live reload"
	@uv run fastapi dev --port 8001

.PHONY: help
help:
	@uv run python -c "import re; \
	[[print(f'\033[36m{m[0]:<20}\033[0m {m[1]}') for m in re.findall(r'^([a-zA-Z_-]+):.*?## (.*)$$', open(makefile).read(), re.M)] for makefile in ('$(MAKEFILE_LIST)').strip().split()]"

.DEFAULT_GOAL := help
