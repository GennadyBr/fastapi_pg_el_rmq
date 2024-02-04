# from logging import getLogger
# from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# from src.api.schemas import DeleteUserResponse
from api.schemas import ShowUser
# from src.api.schemas import UpdatedUserResponse
# from src.api.schemas import UpdateUserRequest
from api.schemas import UserCreate
from db.models import User
from db.session import get_db
from service.auth import get_current_user_from_token
from service.user import _create_new_user
from service.send_email import send_email
# from src.service.user import _delete_user
# from service.user import _get_user_by_id
from service.user import _get_users
# from src.service.user import _update_user
# from src.service.user import check_user_permissions
# from src.settings import settings

# LOGGER = getLogger(__name__)

register_router = APIRouter()

@register_router.post("/", response_model=ShowUser)
async def create_user(body: UserCreate, db: AsyncSession = Depends(get_db)) -> ShowUser:
    # LOGGER.info(f"def create_user({body=}):")
    """Creates a new user with UserCreate body and return ShowUser object"""
    try:
        user = await _create_new_user(body, db)
        await send_email(user=user)
        return user
    except IntegrityError as err:
        # LOGGER.error(err)
        raise HTTPException(status_code=503, detail=f"Database error: {err}")
