# FastAPI Project - Backend

## Requirements

* [Docker](https://www.docker.com/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.
* [make](https://formulae.brew.sh/formula/make) build automation tool


## Build Automation
For build automation, we will be using `make`.
See [makefile](Makefile) for actual commands.


## Database

Install brew postgresql and configures initial database:
```sh
make db-config
```

## Development

Create and activate Virtual Env:
```sh
make venv
source .venv/bin/activate
```

Install all dependencies:
```sh
make install
```

Run dev server with live reload:
```sh
make dev
```

## Linting

Run checks and pre-commit hooks:
```sh
make check
```
Note: Check and fix issues before you commit or else pre-commit hook will fail.

## Testing

Run pytest:
```sh
make test
```

## Coverage HTML

Run coverage report:
```sh
make coverage
```
Note: Make sure coverage is at least 90%


## Other useful commands

To add a new dependency
```sh
uv add <dependency-name>
```
