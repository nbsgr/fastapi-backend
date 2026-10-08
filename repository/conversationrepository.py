#conversationrepository.py
from sqlalchemy import select
from model.conversation import Conversation

#save conversaton
def save(conversation:Conversation,db):
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

#find by id and email (not deleted)
def find_by_id_and_email(conversation_id:int,email:str,db):
    return db.scalar(
        select(Conversation).where(
            Conversation.id==conversation_id,
            Conversation.email == email,
            Conversation.is_deleted==False
        )
    )

#find all active by user email
def find_all_by_email(email:str,db):
    return db.scalars(
        select(Conversation).where(
            Conversation.email == email,
            Conversation.is_deleted==False
        ).order_by(Conversation.last_active_at.desc())
    ).all()