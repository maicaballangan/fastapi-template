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
* [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* [brew](https://brew.sh/) - Package Manager for macOS and Linux
* [make](https://formulae.brew.sh/formula/make) - Build automation tool for macOS and Linux
* [uv](https://docs.astral.sh/uv/) for Python package and environment management

    
```sh
make install
```
See [makefile](Makefile) for build automation commands


## Development

### Database Config

Install brew postgresql and configures initial database:
```sh
make db-config # MacOS
make db-config-linux # for linux
```

### Setup

Create and activate virtual env:
```sh
python3 -m venv .venv
source .venv/bin/activate
```

Copy env and add necessary variables:
```sh
cp .env.local .env
```

Install/sync dependencies:
```sh
make dependencies
```

Run dev server with live reload:
```sh
make dev
```

## Access
http://localhost:8001/docs

username: admin@test.com
password: Admin12#


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
