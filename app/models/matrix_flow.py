from sqlalchemy import Text, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid

from . import Base

class Matrixflow(Base):
    __tablename__ = "matrixflows"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, index=True, server_default=func.gen_random_uuid())
    graph: Mapped[str] = mapped_column(Text)
