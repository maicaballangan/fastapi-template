from http import HTTPStatus
from typing import Annotated

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer

from app.core import security
from app.core.config import settings
from app.models.users import User

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f'{settings.API_V1_STR}/login')

TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(token: TokenDep) -> User:
    user_id = security.verify_token(token, 'access')
    if user_id is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.phrase)
    user = await User.get_or_none(id=user_id)
    if user is None or user.is_active is False:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.phrase)
    return user


async def get_current_user_from_email(token: str) -> User:
    email = security.verify_token(token, 'email')
    if email is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.phrase)
    user = await User.get_by_email(email=email)
    if user is None:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=HTTPStatus.UNAUTHORIZED.phrase)
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]
UserFromEmailToken = Annotated[User, Depends(get_current_user_from_email)]


def get_current_active_superuser(current_user: CurrentUser) -> User:
    if current_user.is_superuser is False:
        raise HTTPException(status_code=HTTPStatus.FORBIDDEN, detail=HTTPStatus.FORBIDDEN.phrase)
    return current_user


SuperUser = Depends(get_current_active_superuser)
