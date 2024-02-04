from typing import List
from typing import Union
from uuid import UUID

from sqlalchemy import and_
from sqlalchemy import select
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

# from db.models import PortalRole
from db.models import User


class UserDAL:
    """Data Access Layer for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    # async def search_users(self, body) -> Union[List[User], None]:
    #
    #     if body.username is not None:
    #         query = select(User).where(User.username == body.username)
    #         res = await self.db_session.execute(query)
    #     if body.email is not None:
    #     if body.fio is not None:
    #     if body.birthday is not None:
    #     if body.tags is not None:
    #
    #     return query.all()


    async def get_user_by_username(self, username: str) -> Union[User, None]:
        """Data Access Layer for getting user by id and return User.user_id or None"""
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]



    async def get_users(self) -> Union[List[User], None]:
        """Data Access Layer for getting user by id and return User.user_id or None"""
        # query = select(User).where(User.user_id == user_id)
        query = select(User)
        res = await self.db_session.execute(query)
        users = res.fetchall()
        if users is not None:
            return users


    async def create_user(
        self,
        username: str,
        email: str,
        password: str,
        config: str,
        # config: dict,
        # roles: list[PortalRole],
    ) -> User:
        """Data Access Layer for creating user and return User object"""
        new_user = User(
            username=username,
            email=email,
            password=password,
            config=config,
            # roles=roles,
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user
    #
    # async def delete_user(self, user_id: UUID) -> Union[UUID, None]:
    #     """Data Access Layer for deleting user and return user_id or None"""
    #     query = (
    #         update(User)
    #         .where(and_(User.user_id == user_id, User.is_active == True))
    #         .values(is_active=False)
    #         .returning(User.user_id)
    #     )
    #     res = await self.db_session.execute(query)
    #     deleted_user_id_row = res.fetchone()
    #     if deleted_user_id_row is not None:
    #         return deleted_user_id_row[0]
    #
    # async def get_user_by_id(self, user_id: UUID) -> Union[User, None]:
    #     """Data Access Layer for getting user by id and return User.user_id or None"""
    #     query = select(User).where(User.user_id == user_id)
    #     res = await self.db_session.execute(query)
    #     user_row = res.fetchone()
    #     if user_row is not None:
    #         return user_row[0]
    #
    # async def get_all_user(self) -> Union[List[User], None]:
    #     """Data Access Layer for getting user by id and return User.user_id or None"""
    #     query = select(User)
    #     res = await self.db_session.execute(query)
    #     user_row = res.fetchall()
    #     if user_row is not None:
    #         return user_row
    #
    # async def get_user_by_email(self, email: str) -> Union[User, None]:
    #     """Data Access Layer for geting user by email, return User.user_id or None"""
    #     query = select(User).where(User.email == email)
    #     res = await self.db_session.execute(query)
    #     user_row = res.fetchone()
    #     if user_row is not None:
    #         return user_row[0]
    #
    # async def update_user(self, user_id: UUID, **kwargs) -> Union[UUID, None]:
    #     """Data Access Layer for updating user by user_id and return user_id or None"""
    #     query = (
    #         update(User)
    #         .where(and_(User.user_id == user_id, User.is_active == True))
    #         .values(kwargs)
    #         .returning(User.user_id)
    #     )
    #     res = await self.db_session.execute(query)
    #     update_user_id_row = res.fetchone()
    #     if update_user_id_row is not None:
    #         return update_user_id_row[0]
