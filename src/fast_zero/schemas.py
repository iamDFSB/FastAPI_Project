from typing import List

from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class ListUsers(BaseModel):
    users: List[UserPublic]


class Token(BaseModel):
    access_token: str
    token_type: str
