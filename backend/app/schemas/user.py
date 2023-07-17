from typing import List, Optional
from uuid import UUID
from pydantic import BaseModel

class UserBase(BaseModel):
    username: str

    class Config:
        orm_mode = True

class UserRegister(UserBase):
    password: str
    register_key: str

class UserAuth(UserBase):
    password: str

class User(UserBase):
    user_id: UUID

    class Config:
        orm_mode = True

class LoginRes(BaseModel):
    access_token: str
    token_type: str