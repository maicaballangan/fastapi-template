from typing import Optional

from tortoise import fields

from app.core import security
from app.models.base import BaseDBModel
from app.schemas.user_schema import UserCreate
from app.schemas.user_schema import UserUpdate


class User(BaseDBModel):
    email = fields.CharField(max_length=100, unique=True)
    first_name = fields.CharField(max_length=100)
    last_name = fields.CharField(max_length=100)
    password = fields.CharField(max_length=255)
    last_login = fields.DatetimeField(null=True)
    is_active = fields.BooleanField(default=False)
    is_staff = fields.BooleanField(default=False)
    is_superuser = fields.BooleanField(default=False)

    def full_name(self) -> str:
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    @classmethod
    async def get_by_email(cls, email: str) -> Optional['User']:
        query = cls.get_or_none(email=email.lower())
        user = await query
        return user

    @classmethod
    async def create(cls, user: UserCreate) -> 'User':
        hashed_password = security.get_password_hash(password=user.password)
        user.password = hashed_password
        user.email = user.email.lower()

        model = cls(**user.model_dump())
        await model.save()
        return model

    @classmethod
    async def update(cls, user: 'User', update: UserUpdate) -> 'User':
        if update.email:
            user.email = update.email
        if update.first_name:
            user.first_name = update.first_name
        if update.last_name:
            user.last_name = update.last_name

        await user.save()
        return user

    class PydanticMeta:
        computed = ['full_name']
        exclude = ['created', 'modified']

    class Meta:
        table = 'user'
