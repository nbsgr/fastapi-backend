#chatmessage.py
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from typing import Optional
from base import Base

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    # Indexes
    __table_args__ = (
        Index("idx_chat_conversation_id", "conversation_id"),
        Index("idx_chat_sent_at", "sent_at"),
    )

    # id
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)

    # conversation_id (Foreign key -> conversations.id)
    conversation_id: Mapped[int] = mapped_column(Integer, ForeignKey("conversations.id"), nullable=False)

    # sender_type (USER or BOT)
    sender_type: Mapped[str] = mapped_column(String(20), nullable=False)

    # content (Standard unbounded Text in PostgreSQL / LONGTEXT in MySQL)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # sent_at
    sent_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())

    # sources (JSON string stored as Text)
    sources: Mapped[Optional[str]] = mapped_column(Text, nullable=True)