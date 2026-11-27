default:
    @just --list

lint:
    uv run --locked ruff format --check .
    uv run --locked ruff check .

format:
    uv run --locked ruff check --fix .
    uv run --locked ruff format .

type:
    uv run --locked ty check

test:
    uv run --locked pytest

build:
    uv build

ci: lint type test build
