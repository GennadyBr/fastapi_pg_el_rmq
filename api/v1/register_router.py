from logging import getLogger
import json
from urllib import request

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import ShowUser
from api.schemas import UserCreate
from db.session import get_db
from service.user import _create_new_user
from service.send_email import send_email

LOGGER = getLogger(__name__)

register_router = APIRouter()

@register_router.post("/", response_model=str)
async def register_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> str:
    """Creates a new user with UserCreate body and return JSON ShowUser object"""
    try:
        user = await _create_new_user(body, db)
        await send_email(user=user)
        response = json.dumps(ShowUser.from_orm(user).dict())
        LOGGER.info(
            f"RESPONSE {response}"
        )
        return response
    except IntegrityError as err:
        LOGGER.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
