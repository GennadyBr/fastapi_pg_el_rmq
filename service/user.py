import json
from typing import Union, List
from uuid import UUID

from fastapi import HTTPException

from api.schemas import ShowUser
from api.schemas import UserCreate, UserSearch
from db.dals import UserDAL
# from db.models import PortalRole
from db.models import User
from .hashing import Hasher

async def _search_users(body: UserSearch, session) -> Union[User, None]:
    """Get a user with user_id and return user_id"""
    async with session.begin():
        user_dal = UserDAL(session)
        users = await user_dal.search_users(
            body=body,
        )
        if users is not None:
            return users


async def _get_users(session) -> Union[List[User], None]:
    """Get a user with user_id and return user_id"""
    async with session.begin():
        user_dal = UserDAL(session)
        users = await user_dal.get_users()
        if users is not None:
            return users


async def _create_new_user(body: UserCreate, session) -> ShowUser:
    """Create a new user with UserCreate body and return ShowUser object"""
    async with session.begin():
        user_dal = UserDAL(session)
        user = await user_dal.create_user(
            username=body.username,
            email=body.email,
            password=Hasher.get_password_hash(body.password),
            config=json.dumps([{
                "fio": body.fio,
                "birthday": body.birthday,
                "tags": body.tags,
            }])
        )
        return ShowUser(
            id=user.id,
            username=user.username,
            config=user.config,
            email=user.email,
            # is_active=user.is_active,
        )
#
#
# async def _delete_user(user_id, session) -> Union[UUID, None]:
#     """Delete a user with user_id and return user_id"""
#     async with session.begin():
#         user_dal = UserDAL(session)
#         deleted_user_id = await user_dal.delete_user(
#             user_id=user_id,
#         )
#         return deleted_user_id
#
#
# async def _update_user(
#     updated_user_params: dict, user_id: UUID, session
# ) -> Union[UUID, None]:
#     """Update a user with user_id and return user_id"""
#     async with session.begin():
#         user_dal = UserDAL(session)
#         updated_user_id = await user_dal.update_user(
#             user_id=user_id, **updated_user_params
#         )
#         return updated_user_id
#
#
# async def _get_user_by_id(user_id, session) -> Union[User, None]:
#     """Get a user with user_id and return user_id"""
#     async with session.begin():
#         user_dal = UserDAL(session)
#         user = await user_dal.get_user_by_id(
#             user_id=user_id,
#         )
#         if user is not None:
#             return user
#
#
# def check_user_permissions(target_user: User, current_user: User) -> bool:
#     """Check if current_user in SuperAdmin and if target_user is current_user"""
#     if PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles:
#         raise HTTPException(
#             status_code=403, detail="Superadmin cannot be deleted via API."
#         )
#     if target_user.user_id != current_user.user_id:
#         # check admin role
#         if not {
#             PortalRole.ROLE_PORTAL_ADMIN,
#             PortalRole.ROLE_PORTAL_SUPERADMIN,
#         }.intersection(current_user.roles):
#             return False
#         # check admin deactivate superadmin attempt
#         if (
#             PortalRole.ROLE_PORTAL_SUPERADMIN in target_user.roles
#             and PortalRole.ROLE_PORTAL_ADMIN in current_user.roles
#         ):
#             return False
#         # check admin deactivate admin attempt
#         if (
#             PortalRole.ROLE_PORTAL_ADMIN in target_user.roles
#             and PortalRole.ROLE_PORTAL_ADMIN in current_user.roles
#         ):
#             return False
#     return True
