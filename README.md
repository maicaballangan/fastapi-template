# FastAPI Project - Backend

This is a FastAPI project template that with Tortoise ORM, Pydantic data validation, alembic migration, and other useful tools like ruff for linting, and pytest + coverage for testing.

```
.
├── app
│   ├── core                        - core classes
│   ├── email-templates             - email templates
│   ├── models                      - tortoise models
│   │   ├── users.py
│   │   └── ...
│   ├── routes                      - api routers
│   │   ├── app_router.py
│   │   ├── auth_router.py
│   │   ├── user_routes.py
│   │   └── ...
│   ├── schemas                     - pydantic schema
│   │   ├── user_schemas.py
│   │   └── ...
│   ├── utils                       - utilities
│   └── main.py
├── tests
│   ├── models                      - model unit tests
│   ├── routes                      - integration tests
│   └── conftest.py
├── Dockerfile          
├── Makefile                        - build automation
└── README.md

```
## Requirements

* [Docker](https://www.docker.com/): 
* [uv](https://docs.astral.sh/uv/) package and env management: `brew install uv`
* [make](https://formulae.brew.sh/formula/make) build automation tool: `brew install make`


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
