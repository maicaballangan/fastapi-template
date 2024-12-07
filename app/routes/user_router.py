from http import HTTPStatus

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi_pagination import Page
from fastapi_pagination import paginate

from app.core import emails
from app.core.authentication import CurrentUser
from app.core.authentication import SuperUser
from app.core.authentication import UserFromEmailToken
from app.core.config import settings
from app.core.security import get_password_hash
from app.core.security import verify_password
from app.models.users import User
from app.schemas.user_schema import ResetPassword
from app.schemas.user_schema import UpdatePassword
from app.schemas.user_schema import UserCreate
from app.schemas.user_schema import UserOut
from app.schemas.user_schema import UserOutAdmin
from app.schemas.user_schema import UserUpdate

router = APIRouter()


@router.post('/register', response_model=UserOut, status_code=HTTPStatus.CREATED, tags=['users'])
async def register_user(
    *,
    user_in: UserCreate,
):
    """
    Create new user.
    """
    existing_user = await User.get_by_email(email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='The user with this email already exists in the system',
        )

    user = await User.create(user_in)

    if settings.emails_enabled and user_in.email:
        email_data = emails.generate_verification_email(email_to=user.email, first_name=user.first_name)

        emails.send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
    return user


@router.get('/current', response_model=UserOut, status_code=HTTPStatus.OK, tags=['users'])
def get_current_user(
    current_user: CurrentUser,
):
    """
    Get current user.
    """
    return current_user


@router.put('/current/password', status_code=HTTPStatus.NO_CONTENT, tags=['users'])
async def update_current_user_password(user_in: UpdatePassword, current_user: CurrentUser):
    """
    Update own password.
    """
    if verify_password(user_in.old_password, current_user.password) is False:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Incorrect password')

    current_user.password = get_password_hash(user_in.new_password_1)
    await current_user.save()


@router.put('/current', response_model=UserOut, status_code=HTTPStatus.OK, tags=['users'])
async def update_current_user(user_in: UserUpdate, current_user: CurrentUser):
    """
    Update own user.
    """
    return await User.update(current_user, user_in)


@router.delete('/current', status_code=HTTPStatus.ACCEPTED, tags=['users'])
async def remove_current_user(current_user: CurrentUser):
    """
    Create deactivate email
    """
    if settings.emails_enabled and current_user.email:
        email_data = emails.generate_remove_account_email(
            email_to=current_user.email, first_name=current_user.first_name
        )

        emails.send_email(
            email_to=current_user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )


@router.get(
    '',
    dependencies=[SuperUser],
    response_model=Page[UserOutAdmin],
    status_code=HTTPStatus.OK,
    tags=['users'],
)
async def get_all_user(
    limit: int = 100,
    offset: int = 0,
):
    """
    Retrieve users.
    """
    users = await User.all().limit(limit).offset(offset)
    return paginate(users)


@router.get(
    '/{id}',
    dependencies=[SuperUser],
    response_model=UserOutAdmin,
    status_code=HTTPStatus.OK,
    tags=['users'],
)
async def get_user(
    id: int,
):
    """
    Get a specific user by id.
    """
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=HTTPStatus.NOT_FOUND.phrase,
        )
    return user


@router.post(
    '',
    dependencies=[SuperUser],
    response_model=UserOutAdmin,
    status_code=HTTPStatus.CREATED,
    tags=['users'],
)
async def create_user(*, user_in: UserCreate):
    """
    Create new user.
    """
    existing_user = await User.get_by_email(email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail='The user with this username already exists in the system',
        )

    hashed_password = get_password_hash(user_in.password)
    db_user = UserCreate(**user_in.create_update_dict(), hashed_password=hashed_password)
    user = await User.create(db_user)
    return user


@router.put(
    '/{id}',
    dependencies=[SuperUser],
    response_model=UserOut,
    status_code=HTTPStatus.OK,
    tags=['users'],
)
async def update_user(
    id: int,
    user_in: UserUpdate,
):
    """
    Update a user.
    """
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=HTTPStatus.NOT_FOUND.phrase)
    if user_in.email:
        user_in.email = user_in.email.lower()
        existing = await User.get_by_email(email=user_in.email)
        if existing:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail='The email already exist in the system',
            )
    user = await user.update(user, user_in)
    return user


@router.delete(
    '/{id}',
    dependencies=[SuperUser],
    status_code=HTTPStatus.NO_CONTENT,
    tags=['users'],
)
async def remove_user(id: int):
    """
    Delete a user
    """
    user = await User.get_or_none(id=id)
    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=HTTPStatus.NOT_FOUND.phrase,
        )
    await user.delete()


@router.post('/verify-email', status_code=HTTPStatus.NO_CONTENT)
async def user_verify_email(user: UserFromEmailToken):
    """
    Verify email
    """
    if user.is_active is True:
        raise HTTPException(
            status_code=HTTPStatus.GONE,
            detail='The user with this email is already verified',
        )
    user.is_active = True
    await user.save()

    if settings.emails_enabled and user.email:
        email_data = emails.generate_welcome_email(first_name=user.first_name)

        emails.send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )


@router.post('/reset-password', status_code=HTTPStatus.NO_CONTENT)
async def user_reset_password(body: ResetPassword, user: UserFromEmailToken):
    """
    Reset password
    """
    if user.is_active is False:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Inactive user')
    hashed_password = get_password_hash(password=body.new_password_1)
    user.password = hashed_password

    await user.save()


@router.post('/verify-delete', status_code=HTTPStatus.NO_CONTENT, tags=['users'])
async def user_verify_delete(user: UserFromEmailToken):
    """
    Deactivate user
    """
    await user.delete()

    if settings.emails_enabled and user.email:
        email_data = emails.generate_remove_account_success_email(first_name=user.first_name)

        emails.send_email(
            email_to=user.email,
            subject=email_data.subject,
            html_content=email_data.html_content,
        )
