# Единые цели для линтеров, форматтеров и тайпчекеров трёх языков.
# Использование: make lint | make fmt | make typecheck | make setup | make precommit

.PHONY: lint lint-go lint-py lint-ts fmt fmt-go fmt-py fmt-ts \
        typecheck typecheck-py typecheck-ts setup setup-go setup-py setup-ts \
        precommit precommit-install

lint: lint-go lint-py lint-ts

fmt: fmt-go fmt-py fmt-ts

typecheck: typecheck-py typecheck-ts

# --- Go ---------------------------------------------------------------------

lint-go:
	golangci-lint run

fmt-go:
	gofmt -w .

# --- Python -----------------------------------------------------------------

lint-py:
	ruff check .
	ruff format --check .

fmt-py:
	ruff format .
	ruff check --fix .

typecheck-py:
	mypy .

# --- TypeScript -------------------------------------------------------------

lint-ts:
	npx eslint .

fmt-ts:
	npx prettier --write .

typecheck-ts:
	npx tsc --noEmit

# --- Установка инструментов (разовые) ---------------------------------------

setup: setup-go setup-py setup-ts

setup-go:
	go install github.com/golangci/golangci-lint/v2/cmd/golangci-lint@latest

setup-py:
	pip install ruff mypy || uv tool install ruff mypy

setup-ts:
	# typescript-eslint@8 поддерживает TypeScript до 6.1 — поэтому фиксируем 5.9
	npm install --save-dev eslint @eslint/js typescript-eslint prettier "typescript@~5.9.0"

# --- Pre-commit -------------------------------------------------------------

precommit-install:
	pip install pre-commit && pre-commit install

precommit:
	pre-commit run --all-files
