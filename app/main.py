from contextlib import asynccontextmanager
from http import HTTPStatus

import sentry_sdk
from fastapi import FastAPI
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.routing import APIRoute
from fastapi.routing import APIRouter
from fastapi_pagination import add_pagination
from tortoise.contrib.fastapi import register_tortoise
from tortoise.exceptions import DoesNotExist

from app.core.config import settings
from app.routes import app_router
from app.routes import auth_router
from app.routes import user_router


def custom_generate_unique_id(route: APIRoute) -> str:
    return f'{route.tags[0]}-{route.name}'


if settings.SENTRY_DSN and settings.ENVIRONMENT != 'local':
    sentry_sdk.init(dsn=str(settings.SENTRY_DSN), enable_tracing=True)

# setup database
MODELS = [
    'aerich.models',
    'app.models.user',
]

TORTOISE_ORM = {
    'connections': {
        # Dict format for connection
        'default': {
            'engine': 'tortoise.backends.asyncpg',
            'credentials': {
                'host': settings.POSTGRES_SERVER,
                'port': settings.POSTGRES_PORT,
                'user': settings.POSTGRES_USER,
                'password': settings.POSTGRES_PASSWORD,
                'database': settings.POSTGRES_DB,
            },
        }
    },
    'apps': {'app': {'models': MODELS}},
    'use_tz': False,
    'timezone': 'UTC',
}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # do sth before db inited
    async with register_tortoise(
        app,
        add_exception_handlers=True,
    ):
        yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f'{settings.API_V1_STR}/openapi.json',
    generate_unique_id_function=custom_generate_unique_id,
    lifespan=lifespan,
)


# Set all CORS enabled origins
if settings.all_cors_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.all_cors_origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

api_router = APIRouter()
api_router.include_router(app_router.router, tags=['utils'])
api_router.include_router(auth_router.router, tags=['auth'])
api_router.include_router(user_router.router, prefix='/users', tags=['users'])
app.include_router(api_router, prefix=settings.API_V1_STR)
add_pagination(app)


# Global Exception
@app.exception_handler(DoesNotExist)
async def validation_exception_handler(request, exc):
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND,
        detail=HTTPStatus.NOT_FOUND.phrase,
    )
