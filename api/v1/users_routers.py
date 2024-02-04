# from logging import getLogger
# from uuid import UUID
import json
from typing import List

from fastapi import APIRouter, Query
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_

# from src.api.schemas import DeleteUserResponse
from api.schemas import ShowUser
# from src.api.schemas import UpdatedUserResponse
# from src.api.schemas import UpdateUserRequest
# from src.api.schemas import UserCreate
from db.models import User
from db.session import get_db
from service.auth import get_current_user_from_token
# from src.service.user import _create_new_user
# from src.service.user import _delete_user
# from service.user import _get_user_by_id
from service.user import _get_users

# from src.service.user import _update_user
# from src.service.user import check_user_permissions
# from src.settings import settings

# LOGGER = getLogger(__name__)

users_router = APIRouter()


@users_router.get("/", response_model=List[ShowUser])
async def get_users(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> List[ShowUser]:
    """Get list of users return ShowUser objects"""
    # LOGGER.info(f"def get_user_by_id({user_id=}, {current_user=}):")
    # users = await _get_users(db)
    users = [raw[0] for raw in await _get_users(db)]
    if users is None:
        raise HTTPException(
            status_code=404, detail=f"Users not found."
        )
    return users


@users_router.get("/search")
async def search_users(
        db: AsyncSession = Depends(get_db),
        username: str = Query(None),
        email: str = Query(None),
        fio: str = Query(None),
        birthday: str = Query(None),
        tags: str = Query(None)
):
        query = select(User)
        if username is not None:
            # query = select(User).where(User.username == username)
            stmt = \
                f"""
                SELECT *
                FROM users
                WHERE username = '{username}'
                ;
                """
            result = await db.execute(stmt)
            a = result.fetchall()
            # result = result.scalars().first()
            return a
        if email is not None:
            query = select(User).where(and_(User.email == email, User.username == username))
        if fio is not None:
            # query = select(User).where(User.config.any([{'fio': fio}]))
            # query = select(User).where(User.config.params(['fio']).astext)
            # val = db.column('value', type_=JSONB)
            path = f"$.** ? (@.{fio})"
            # stmt = \
            #     f"""
            #     SELECT jsonb_path_query(record_map,
            #         'strict $.**?(@.keyvalue().key==$target_id)',
            #         jsonb_build_object('target_id',
            #                            '7a9abf0d-a066-4466-a565-4e6d7a960a37'))
            #     FROM private_notion
            #     WHERE site_id = '45bf37be-ca0a-45eb-838b-015c7a89d47b';
            #     """
            #
            #
            # result = await db.execute(stmt)
            # result = result.scalars().first()


        if birthday is not None:
            query = select(User).where(User.config["birthday"] == birthday)
        if tags is not None:
            query = select(User).where(User.config["tags"] == tags)

        res = await db.execute(query)
        user_row = res.fetchall()
        if user_row is not None:
            return user_row


# @user_router.get("/", response_model=ShowUser)
# async def get_user_by_id(
#     user_id: UUID,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token),
# ) -> ShowUser:
#     """Get user by id and return ShowUser object"""
#     LOGGER.info(f"def get_user_by_id({user_id=}, {current_user=}):")
#     user = await _get_user_by_id(user_id, db)
#     if user is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     return user

#
#
#
# @user_router.delete("/", response_model=DeleteUserResponse)
# async def delete_user(
#     user_id: UUID,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token),
# ) -> DeleteUserResponse:
#     """Deletes a user with user_id and return DeleteUserResponse object"""
#     LOGGER.info(f"def delete_user({user_id=}, {current_user=}):")
#     user_for_deletion = await _get_user_by_id(user_id, db)
#     if user_for_deletion is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     if not check_user_permissions(
#         target_user=user_for_deletion,
#         current_user=current_user,
#     ):
#         raise HTTPException(status_code=403, detail="Forbidden.")
#     deleted_user_id = await _delete_user(user_id, db)
#     if deleted_user_id is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     return DeleteUserResponse(deleted_user_id=deleted_user_id)
#
#
# @user_router.patch("/", response_model=UpdatedUserResponse)
# async def update_user_by_id(
#     user_id: UUID,
#     body: UpdateUserRequest,
#     db: AsyncSession = Depends(get_db),
#     current_user: User = Depends(get_current_user_from_token),
# ) -> UpdatedUserResponse:
#     """Update user by user_id and UpdateUserRequest body and return UpdatedUserResponse object"""
#     LOGGER.info(f"def update_user_by_id({user_id=}, {body=}, {current_user=}):")
#     updated_user_params = body.dict(exclude_none=True)
#     if updated_user_params == {}:
#         raise HTTPException(
#             status_code=422,
#             detail="At least one parameter for user update info should be provided",
#         )
#     user_for_update = await _get_user_by_id(user_id, db)
#     if user_for_update is None:
#         raise HTTPException(
#             status_code=404, detail=f"User with id {user_id} not found."
#         )
#     if user_id != current_user.user_id:
#         if check_user_permissions(
#             target_user=user_for_update, current_user=current_user
#         ):
#             raise HTTPException(status_code=403, detail="Forbidden.")
#     try:
#         updated_user_id = await _update_user(
#             updated_user_params=updated_user_params, session=db, user_id=user_id
#         )
#     except IntegrityError as err:
#         LOGGER.error(err)
#         raise HTTPException(status_code=503, detail=f"Database error: {err}")
#     return UpdatedUserResponse(updated_user_id=updated_user_id)
