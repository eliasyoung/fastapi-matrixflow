from sqlalchemy import Text
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from . import Base

class Matrixflow(Base):
    __tablename__ = "matrixflows"

    id: Mapped[str] = mapped_column(UUID, primary_key=True, index=True)
    graph: Mapped[str] = mapped_column(Text)
