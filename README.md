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
* [brew](https://brew.sh/) - Package Manager for macOS and Linux
* [make](https://formulae.brew.sh/formula/make) - Build automation tool for macOS and Linux
* [Python 3.11](https://www.python.org/downloads/release/python-3110/)
* [uv](https://docs.astral.sh/uv/) Package Manager for python
* Postgres

```sh
brew install make
brew install python@3.11
brew install uv
brew install postgresql
```

## Development

### Database Config

Install postgresql:
```sh
# Mac
brew install postgresql
brew services start postgresql

# Linux
sudo apt-get update
sudo apt-get install postgresql
sudo service postgresql start
```

Configure database:
```sh
createuser -s postgres
psql -U postgres -f data/create_superuser.sql
```

### Setup

Note: See [makefile](Makefile) for build automation commands

Create and activate virtual env:
```sh
make venv
source .venv/bin/activate
```

Copy env and add necessary variables:
```sh
cp .env.local .env
```

Install/sync dependencies:
```sh
make install
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
make lint
```

## Other useful commands

To add a new dependency
```sh
uv add <dependency-name>
```
