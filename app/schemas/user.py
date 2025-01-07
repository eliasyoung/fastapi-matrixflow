import uuid
from typing import Union, Optional
from datetime import datetime
from enum import Enum
import phonenumbers

from pydantic import BaseModel, EmailStr, ConfigDict, Field
from pydantic_extra_types.phone_numbers import PhoneNumber

class RoleEnum(Enum):
    ADMIN = 'admin'
    USER = 'user'

    def can_do_anything(self):
        return self == RoleEnum.ADMIN

    def can_view(self):
        return self in [RoleEnum.ADMIN, RoleEnum.USER]


class GetUserResponse(BaseModel):
    id: uuid.UUID
    username: str
    email: Union[EmailStr, None] = None
    phone: Union[str, None] = None
    is_active: bool
    role: RoleEnum
    created_at: datetime
    updated_at: datetime


class User(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    username: str = Field(min_length=5)
    email: Union[EmailStr, None] = None
    phone: Union[PhoneNumber, None] = None
    is_active: bool
    role: RoleEnum
    created_at: datetime
    updated_at: datetime

    def to_response(self) -> GetUserResponse:
        data = self.dict()

        if self.phone is not None:
            phone = phonenumbers.parse(self.phone, None)
            phone = phonenumbers.format_number(phone, phonenumbers.PhoneNumberFormat.E164)
            data.update({"phone": phone})

        return GetUserResponse(**data)


class UserInDB(User):
    hashed_password: str


class GetByUsernamePayload(BaseModel):
    username: str


class CreateUserPayload(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=6)
    email: Optional[EmailStr] = None
    phone: Optional[PhoneNumber] = None
    role: Optional[RoleEnum] = RoleEnum.USER

class AuthenticateUserPayload(BaseModel):
    username: str = Field(min_length=5)
    password: str = Field(min_length=6)
