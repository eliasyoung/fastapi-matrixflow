from fastapi import APIRouter, HTTPException

from app.crud.user import get_user_by_username, create_user
from app.api.dep import DBSessoinDep, CurrentUserDep
from app.schemas.user import GetByUsernamePayload, CreateUserPayload, User,AuthenticateUserPayload, GetUserResponse
from app.schemas.api import CustomJSONResponse
from app.core.security import get_password_hash

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/")
async def get_user_by_name(db_session: DBSessoinDep, payload:GetByUsernamePayload):
    user = await get_user_by_username(db_session, payload.username)

    if not user:
        raise HTTPException(status_code=404, detail="user not found")

    user = User.from_orm(user).to_response()

    return CustomJSONResponse(
        code=0,
        data=user
    )

    return user

@router.post("/")
async def signup_user(db_session: DBSessoinDep, payload: CreateUserPayload):
    hashed_password = get_password_hash(payload.password)
    payload.password = hashed_password

    new_user = await create_user(db_session, payload)
    await db_session.commit()
    await db_session.refresh(new_user)

    user = User.from_orm(new_user).to_response()

    return CustomJSONResponse(
        code=0,
        data=user
    )

@router.get("/me", response_model=CustomJSONResponse[GetUserResponse])
async def get_me(current_user: CurrentUserDep):

    user = current_user.to_response()

    return CustomJSONResponse(
        code=0,
        data=user
    )
