# FastAPI Template

```
.
├── app
│   ├── core                        - core classes
│   ├── email-templates             - email templates
│   ├── models                      - tortoise models
│   │   ├── user.py
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

* [Docker](https://www.docker.com/).
* [uv](https://docs.astral.sh/uv/) for Python package and environment management.
* [make](https://formulae.brew.sh/formula/make) build automation tool


Note: See [makefile](Makefile) for build automation commands

## Docker Deployment
```sh
sudo docker compose up
```

## Access
http://localhost:8001/docs


## Development

### Database Config

Install brew postgresql and configures initial database:
```sh
make db-config
```

### Setup

Create and activate virtual env:
```sh
make venv
source .venv/bin/activate
```

Copy env and add necessary variables:
```sh
cp .env.local .env
```

Install all dependencies:
```sh
make install
```

Run dev server with live reload:
```sh
make dev
```

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

## Lint Fix

Check and fix issues before you commit or else pre-commit hook will fail:
```sh
make fix
```

## Other useful commands

To add a new dependency
```sh
uv add <dependency-name>
```
