from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert

from app.schemas.user import CreateUserPayload
from app.models import UserModel

async def get_user_by_username(db_session: AsyncSession, username: str) -> UserModel | None:
    user = (await db_session.scalars(select(UserModel).where(UserModel.username == username))).first()

    return user

async def create_user(db_session: AsyncSession, create_workflow_payload: CreateUserPayload) -> UserModel:
    insert_data = create_workflow_payload.dict()

    result = await db_session.execute(insert(UserModel).values(**insert_data).returning(UserModel))

    new_user = result.scalar_one()

    return new_user
