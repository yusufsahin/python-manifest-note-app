from datetime import datetime
from sqlalchemy import String, JSON, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base

class Record(Base):
    __tablename__ = "records"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(String(64), index=True)
    data: Mapped[dict] = mapped_column(JSON, default=dict)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now())
