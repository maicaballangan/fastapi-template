from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import model_validator
from sqlmodel import Field


class BaseUserInput(BaseModel):
    def create_update_dict(self):
        return self.model_dump(
            exclude_unset=True,
            exclude={'id', 'is_superuser', 'is_active'},
        )

    def create_update_dict_superuser(self):
        return self.model_dump(exclude_unset=True, exclude={'id'})


class UserCreate(BaseUserInput):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: EmailStr = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8, max_length=40)


class UserUpdate(BaseUserInput):
    first_name: str = Field(default=None, min_length=1, max_length=100)
    last_name: str = Field(default=None, min_length=1, max_length=100)
    email: EmailStr = Field(default=None, max_length=100)


class UpdatePassword(BaseModel):
    old_password: str = Field(min_length=8, max_length=40)
    new_password_1: str = Field(min_length=8, max_length=40)
    new_password_2: str = Field(min_length=8, max_length=40)

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'UpdatePassword':
        if self.new_password_1 != self.new_password_2:
            raise ValueError('passwords do not match')
        if self.new_password_1 == self.old_password:
            raise ValueError('new password should not be the same current')
        return self


class ResetPassword(BaseModel):
    new_password_1: str = Field(min_length=8, max_length=40)
    new_password_2: str = Field(min_length=8, max_length=40)

    @model_validator(mode='after')
    def check_passwords_match(self) -> 'ResetPassword':
        if self.new_password_1 != self.new_password_2:
            raise ValueError('passwords do not match')
        return self


class UserOutputPublic(BaseModel):
    first_name: str | None
    last_name: str | None
    email: EmailStr | None = None


# User public output
class UserOutput(UserOutputPublic):
    id: int
    is_active: bool
    is_superuser: bool


class UserDB(UserOutputPublic):
    password: str | None
    is_active: bool | None = True
    is_superuser: bool | None = False
