from typing import Annotated

from app.database import get_db_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

DBSessoinDep = Annotated[AsyncSession, Depends(get_db_session)]