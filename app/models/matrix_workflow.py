import uuid
from datetime import datetime

from sqlalchemy import Text, text, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP

from . import Base

class MatrixWorkflow(Base):
    __tablename__ = "matrix_workflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, server_default=text('gen_random_uuid()'))
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    graph: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=False, server_default=text('CURRENT_TIMESTAMP'), onupdate=datetime.now())
