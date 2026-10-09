# ==========================================
# CHAT MESSAGE REPOSITORY
# ==========================================
from sqlalchemy import select
from model.chatmessage import ChatMessage

# ==========================================
# SAVE MESSAGE
# ==========================================
def save(message: ChatMessage, db):
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

# ==========================================
# FIND ALL BY CONVERSATION (CHRONOLOGICAL ORDER BY ID)
# ==========================================
def find_by_conversation_id(id: int, db):
    return db.scalars(
        select(ChatMessage).where(
            ChatMessage.conversation_id == id
        ).order_by(ChatMessage.id.asc())
    ).all()

# ==========================================
# FIND RECENT BY CONVERSATION ID (FOR AI CONTEXT)
# ==========================================
def find_recent_by_conversation_id(id: int, limit: int, db):
    return db.scalars(
        select(ChatMessage).where(
            ChatMessage.conversation_id == id
        ).order_by(ChatMessage.id.desc()).limit(limit)
    ).all()