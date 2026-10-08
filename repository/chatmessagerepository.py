#chatmessagerepository
from sqlalchemy import select
from model.chatmessage import ChatMessage

#save chatmessage
def save(message:ChatMessage,db):
    db.add(message)
    db.commit()
    db.refresh(message)
    return message

#Find all by conversation (Chronological order)
def find_by_conversation_id(id:int,db):
    return db.scalars(
        select(ChatMessage).where(
            ChatMessage.conversation_id==id
        ).order_by(ChatMessage.sent_at.asc())
    ).all()

#find recent messages (for Ai context Window)

def find_recent_by_conversation_id(id:int,limit:int,db):
    return db.scalars(
        select(ChatMessage).where(
            ChatMessage.conversation_id==id
        ).order_by(ChatMessage.sent_at.desc()).limit(limit)
    ).all()