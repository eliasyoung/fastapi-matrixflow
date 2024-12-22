import uuid
from datetime import datetime

from sqlalchemy import Text, text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
import uuid

from . import Base

class Matrixflow(Base):
    __tablename__ = "matrixflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, server_default=text('gen_random_uuid()'))
    graph: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), server_onupdate=text('CURRENT_TIMESTAMP'))

