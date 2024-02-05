from logging import getLogger
from typing import Union, List

from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowUser
from api.schemas import UserCreate, UserSearch
from db.crud import UserCRUD
from db.models import User
from .hashing import Hasher

LOGGER = getLogger(__name__)

async def _delete_user(id: int, session: AsyncSession) -> Union[User, None]:
    """Delete a user with id and return user"""
    # LOGGER.info(f"Delete user {id=}")
    async with session.begin():
        user_dal = UserCRUD(session)
        deleted_user = await user_dal.delete_user(
            id=id,
        )
        return deleted_user



async def _search_users(body: UserSearch, session: AsyncSession) -> Union[List[User], User, None]:
    """Search a user with body UserSearch and return users"""
    # LOGGER.info(f"_search_users {body.dict()=}")
    async with session.begin():
        user_dal = UserCRUD(session)
        users = await user_dal.search_users(
            body=body,
        )
        if users is not None:
            return users


async def _get_users(session: AsyncSession) -> Union[List[User], User, None]:
    """Get a users"""
    # LOGGER.info("Get users")
    async with session.begin():
        user_dal = UserCRUD(session)
        users = await user_dal.get_users()
        if users is not None:
            return users


async def _create_new_user(body: UserCreate, session: AsyncSession) -> ShowUser:
    """Create a new user with UserCreate body and return ShowUser object"""
    # LOGGER.info(f"Create new user {body.dict()=}")
    async with session.begin():
        user_dal = UserCRUD(session)
        user = await user_dal.create_user(
            username=body.username,
            email=body.email,
            password=Hasher.get_password_hash(body.password),
            config={
                "fio": body.fio,
                "birthday": body.birthday,
                "tags": body.tags,
            })

        return ShowUser(
            id=user.id,
            username=user.username,
            config=user.config,
            email=user.email,
        )
