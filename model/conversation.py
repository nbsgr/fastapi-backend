#conversation.py
from sqlalchemy import Integer, String, Boolean, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from base import Base

class Conversation(Base):
    __tablename__ = "conversations"

    # Indexes
    __table_args__ = (
        Index("idx_conversation_email", "email"),
        Index("idx_conversation_created_at", "created_at"),
    )

    # id
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # email (Foreign key -> users.email)
    email: Mapped[str] = mapped_column(String(255), ForeignKey("users.email"), nullable=False)

    # title
    title: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)

    # is_deleted (soft delete)
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    # deleted_at
    deleted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    # created_at
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # last_active_at
    last_active_at: Mapped[Optional[datetime]] = mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=True)