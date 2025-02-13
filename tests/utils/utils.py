import random
import string

from app.models.user import User
from app.schemas.user_schema import UserDB


def random_lower_string() -> str:
    return ''.join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f'{random_lower_string()}@askmagna.com'


async def user_mock() -> User:
    user_in = UserDB(
        first_name=random_lower_string(),
        last_name=random_lower_string(),
        email=random_email(),
        password='mockpassword',
        is_active=True,
        is_superuser=False,
    )
    user = await User.create(user=user_in)
    return user


async def inactive_user_mock() -> User:
    user_in = UserDB(
        first_name=random_lower_string(),
        last_name=random_lower_string(),
        email=random_email(),
        password='mockpassword',
        is_active=False,
        is_superuser=False,
    )
    user = await User.create(user=user_in)
    return user
