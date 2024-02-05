from logging import getLogger
import json

from fastapi import APIRouter, Query
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowUser
from db.models import User
from db.session import get_db
from service.auth import get_current_user_from_token

from service.user import _delete_user

LOGGER = getLogger(__name__)

user_delete_router = APIRouter()


@user_delete_router.delete("/", response_model=str)
async def user_delete(
        id: int = Query(None),
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user_from_token),
) -> str:
    """Delete user with id and return JSON ShowUser object"""
    # LOGGER.info(f"def create_user({id=}):")
    try:
        users = await _delete_user(id, db)
        if not users:
            return "User not found"
        else:
            response = json.dumps([ShowUser.from_orm(user).dict() for user in users])
            LOGGER.info(
                f"RESPONSE {response}"
            )
            return response
    except IntegrityError as err:
        LOGGER.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
