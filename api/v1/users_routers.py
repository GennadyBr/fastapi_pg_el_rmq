from logging import getLogger
import json

from fastapi import APIRouter, Query
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowUser, UserSearch
from db.models import User
from db.session import get_db
from service.auth import get_current_user_from_token
from service.user import _get_users, _search_users

LOGGER = getLogger(__name__)

users_router = APIRouter()


@users_router.get("/", response_model=str)
async def get_users(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> str:
    """Get list of users return JSON ShowUser objects"""
    # LOGGER.info(f"def get_users")
    users = [ShowUser.from_orm(raw[0]).dict() for raw in await _get_users(db)]
    if users is None:
        raise HTTPException(
            status_code=404, detail=f"Users not found."
        )
    response = json.dumps(users)
    LOGGER.info(
        f"RESPONSE {response}"
    )
    return response



@users_router.get("/search", response_model=str)
async def search_users(
        username: str = Query(None),
        email: str = Query(None),
        fio: str = Query(None),
        birthday: str = Query(None),
        tags: str = Query(None),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> str:
    """Get Users return JSON ShowUser objects"""
    body = UserSearch(
        username=username,
        email=email,
        fio=fio,
        birthday=birthday,
        tags=tags
    )
    # LOGGER.info(f"def get_user: {body.dict()}")

    users = [ShowUser.from_orm(user).dict() for user in await _search_users(body, db)]
    if users is None:
        raise HTTPException(
            status_code=404, detail=f"Users not found."
        )
    response = json.dumps(users)
    LOGGER.info(
        f"RESPONSE {response}"
    )
    return response

