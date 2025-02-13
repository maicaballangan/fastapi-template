import pytest
from httpx import ASGITransport
from httpx import AsyncClient
from tortoise import Tortoise

from app.core.config import settings
from app.main import app
from app.models.user import User
from app.schemas.user_schema import UserDB
from tests.utils.utils import random_email
from tests.utils.utils import random_lower_string

DB_URL = 'sqlite://:memory:'


async def init_db(db_url, create_db: bool = False, schemas: bool = False) -> None:
    """Initial database connection"""
    await Tortoise.init(db_url=db_url, modules={'models': ['app.models.user']}, _create_db=create_db)
    if create_db:
        print(f'Database created! {db_url = }')
    if schemas:
        await Tortoise.generate_schemas()
        print('Success to generate schemas')


async def init(db_url: str = DB_URL):
    await init_db(db_url, True, True)


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture(scope='session')
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as client:
        yield client


@pytest.fixture(scope='session', autouse=True)
async def initialize_tests():
    await init()
    yield
    await Tortoise._drop_databases()


@pytest.fixture(scope='session')
async def normal_user():
    user_in = UserDB(
        first_name=random_lower_string(),
        last_name=random_lower_string(),
        email=random_email(),
        password='mockpassword',
        is_active=True,
    )

    user = await User.create(user=user_in)
    return user


@pytest.fixture(scope='session')
async def super_user():
    user_in = UserDB(
        first_name=random_lower_string(),
        last_name=random_lower_string(),
        email=random_email(),
        password='mockpassword',
        is_active=True,
        is_superuser=True,
    )

    user = await User.create(user=user_in)
    return user


@pytest.fixture(scope='session')
async def superuser_token_headers(client: AsyncClient, super_user: User):
    data = {'username': super_user.email, 'password': 'mockpassword'}
    r = await client.post(f'{settings.API_V1_STR}/login', data=data)
    token = r.json()['access_token']
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture(scope='session')
async def normaluser_token_headers(client: AsyncClient, normal_user: User):
    data = {'username': normal_user.email, 'password': 'mockpassword'}
    r = await client.post(f'{settings.API_V1_STR}/login', data=data)

    token = r.json()['access_token']
    return {'Authorization': f'Bearer {token}'}
