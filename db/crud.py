from logging import getLogger
from typing import List
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import UserSearch
from db.models import User

LOGGER = getLogger(__name__)

class UserCRUD:
    """CRUD for operating user info"""

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def delete_user(self, id: int) -> Union[User, None]:
        """Deleting user and return user_id or None"""
        # LOGGER.info(f"def delete_user({id=}):")
        body = UserSearch(id=id, fio=None, username=None, email=None)
        deleted_user = await self.search_users(body)
        if deleted_user is None:
            raise
        try:
            query = (
                User.__table__.delete()
                .where(User.id == id)
                .returning(User)
            )
            res = await self.db_session.execute(query)
        except Exception as e:
            pass
        finally:
            return deleted_user

    async def search_users(self, body) -> Union[List[User], User, None]:
        """Search user and return List of User or None"""
        # LOGGER.info(f"def search_user({body.dict()=}):")
        if body.id is not None:
            where_query = f"""
            WHERE id = '{body.id}'
            """
        elif body.username is not None:
            where_query = f"""
            WHERE username = '{body.username}'
            """
        elif body.email is not None:
            where_query = f"""
            WHERE email='{body.email}'
            """
        elif body.fio is not None:
            where_query = f"""
            WHERE config->>'fio'='{body.fio}'
            """
        elif body.birthday is not None:
            where_query = f"""
            WHERE config->>'birthday'='{body.birthday}'
            """
        elif body.tags is not None:
            where_query = f"""
            WHERE config->>'tags'='{body.tags}'
            """
        query = \
            f"""
        SELECT *
        FROM users
        {where_query}
        ;
        """

        res = await self.db_session.execute(query)
        users = res.fetchall()
        # parse cursor result to ORM model for futher JSON serialization
        new_users = []
        for i in users:
            user: User = User(**i)
            new_users.append(user)
        return new_users

    async def get_user_by_username(self, username: str) -> Union[User, None]:
        """Getting user by id and return User or None"""
        # LOGGER.info(f"def search_user({username=}):")
        query = select(User).where(User.username == username)
        res = await self.db_session.execute(query)
        user_row = res.fetchone()
        if user_row is not None:
            return user_row[0]

    async def get_users(self) -> Union[List[User], None]:
        """Getting users list"""
        # LOGGER.info(f"def get_users():")
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
        """Creating user and return User object"""
        new_user = User(
            username=username,
            email=email,
            password=password,
            config=config,
            # roles=roles,
        )
        # LOGGER.info(f"def create_user({new_user.__dict__=}):")
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

