from typing import Union

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose import JWTError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from db.dals import UserDAL
from db.models import User
from db.session import get_db
from .hashing import Hasher
from settings import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def _get_user_by_username_for_auth(
    username: str, session: AsyncSession
) -> Union[User, None]:
    """Get user by email for authentication, return User.user_id"""
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.get_user_by_username(
            username=username,
        )
        return user


async def authenticate_user(
    username: str, password: str, db: AsyncSession
) -> Union[User, None]:
    """Authenticate user by email and password with session, return user"""
    user = await _get_user_by_username_for_auth(username=username, session=db)
    if user is None:
        return
    if not Hasher.verify_password(password, user.password):
        return
    return user


async def get_current_user_from_token(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)
):
    """Get current user from token and session, return user"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = await _get_user_by_username_for_auth(username=username, session=db)
    if user is None:
        raise credentials_exception
    return user
