from datetime import timedelta
from logging import getLogger

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from api.schemas import Token
from db.session import get_db
from service.auth import authenticate_user
from service.security import create_access_token
from settings import settings

LOGGER = getLogger(__name__)
login_router = APIRouter()


@login_router.post("/", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: AsyncSession = Depends(get_db)
):
    """Login for access token and return dict with token and bearer"""
    # LOGGER.info(f"def login_for_access_token({form_data=}):")
    user = await authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "other_custom_data": [1, 2, 3, 4]},
        expires_delta=access_token_expires,
    )
    response = {"access_token": access_token, "token_type": "bearer"}
    LOGGER.info(
        f"RESPONSE {response}"
    )
    return {"access_token": access_token, "token_type": "bearer"}
