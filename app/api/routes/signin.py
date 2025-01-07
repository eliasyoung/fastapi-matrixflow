from datetime import timedelta

from fastapi import APIRouter, HTTPException

from app.api.dep import DBSessoinDep
from app.schemas.user import AuthenticateUserPayload
from app.schemas.token import Token
from app.crud.user import get_user_by_username
from app.core.security import verify_password, create_access_token
from app.settings import settings

router = APIRouter(prefix="/signin", tags=["signin"])

@router.post("/authenticate")
async def authenticate_user_credentials(db_session: DBSessoinDep, payload: AuthenticateUserPayload):
    user = await get_user_by_username(db_session, payload.username)

    if not user:
            raise HTTPException(status_code=400, detail="credentials provided not correct!")

    if not user.is_active:
            raise HTTPException(status_code=400, detail="Inactive user")

    plain_password = payload.password
    hashed_password = user.password
    if not verify_password(plain_password, hashed_password):
        raise HTTPException(status_code=401, detail="credentials provided not correct!")

    access_token_expires = timedelta(minutes=settings.access_token_expire_minutes)

    return Token(
        access_token=create_access_token(
            user.id, expires_delta=access_token_expires
        )
    )
