import uuid
from datetime import datetime, date
from typing import Optional, List
from fastapi import HTTPException
from pydantic import BaseModel, EmailStr, constr, validator, Field, Json


class TunedModel(BaseModel):
    class Config:
        """Tells pydantic to convert even non dict obj to json"""

        orm_mode = True


class ShowUser(TunedModel):
    id: int
    username: str
    email: EmailStr
    config: str
    # config: dict


class UserCreate(BaseModel):
    username: str = Field(example="abcd12", min_length=6, max_length=36)
    email: EmailStr = Field(example="bgs12@mail.ru")
    password: str = Field(example="<PASSWORD>")
    fio: str = Field(example="Иван Иванов", min_length=2, max_length=200)
    birthday: str = Field(example="2020-01-01", min_length=2, max_length=10)
    tags: List[str] = Field(example=["трейдер", "менеджер", "брокер"])


class UserSearch(BaseModel):
    username: str = Optional, Field(example="abcd12", min_length=6, max_length=36)
    email: EmailStr = Optional, Field(example="bgs12@mail.ru")
    fio: str = Optional, Field(example="Иван Иванов", min_length=2, max_length=200)
    birthday: str = Optional, Field(example="2020-01-01", min_length=2, max_length=10)
    tags: List[str] = Optional, Field(example=["трейдер", "менеджер", "брокер"])


#
#     @validator("name")
#     def validate_name(cls, value):
#         if not LETTER_MATCH_PATTERN.match(value):
#             raise HTTPException(
#                 status_code=422, detail="Name should contains only letters"
#             )
#         return value
#
#     @validator("surname")
#     def validate_surname(cls, value):
#         if not LETTER_MATCH_PATTERN.match(value):
#             raise HTTPException(
#                 status_code=422, detail="Surname should contains only letters"
#             )
#         return value
#
#
# class DeleteUserResponse(BaseModel):
#     deleted_user_id: uuid.UUID
#
#
# class UpdatedUserResponse(BaseModel):
#     updated_user_id: uuid.UUID
#
#
# class UpdateUserRequest(BaseModel):
#     name: Optional[constr(min_length=1)]
#     surname: Optional[constr(min_length=1)]
#     email: Optional[EmailStr]
#
#     @validator("name")
#     def validate_name(cls, value):
#         if not LETTER_MATCH_PATTERN.match(value):
#             raise HTTPException(
#                 status_code=422, detail="Name should contains only letters"
#             )
#         return value
#
#     @validator("surname")
#     def validate_surname(cls, value):
#         if not LETTER_MATCH_PATTERN.match(value):
#             raise HTTPException(
#                 status_code=422, detail="Surname should contains only letters"
#             )
#         return value
#
#
class Token(BaseModel):
    access_token: str
    token_type: str
