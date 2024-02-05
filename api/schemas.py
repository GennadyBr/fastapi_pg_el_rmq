from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class TunedModel(BaseModel):
    class Config:
        """Tells pydantic to convert even non dict obj to json"""
        orm_mode = True


class ShowUser(TunedModel):
    id: Optional[int]
    username: Optional[str]
    email: Optional[EmailStr]
    config: Optional[dict]


class UserCreate(BaseModel):
    username: str = Field(example="abcd12", min_length=6, max_length=36)
    email: EmailStr = Field(example="bgs12@mail.ru")
    password: str = Field(example="abcd12")
    fio: str = Field(example="Ivan Ivanov", min_length=2, max_length=200)
    birthday: str = Field(example="2020-01-01", min_length=2, max_length=10)
    tags: str = Field(example="trader,manager,broker")


class UserSearch(BaseModel):
    id: Optional[int] = None
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    fio: Optional[str] = None
    birthday: Optional[str] = None
    tags: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
