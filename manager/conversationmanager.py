#conversationmanager.py
from datetime import datetime
from base import Session
from model.conversation import Conversation
from repository import conversationrepository as cr

# ==========================================
# SERIALIZER HELPER
# ==========================================
def to_dict(c: Conversation):
    if not c:
        return None
    return {
        "id": c.id,
        "email": c.email,
        "user_email": c.email,
        "title": c.title,
        "is_deleted": c.is_deleted,
        "created_at": c.created_at.isoformat() if c.created_at else None,
        "last_active_at": c.last_active_at.isoformat() if c.last_active_at else None,
    }

# ==========================================
# CREATE CONVERSATION
# ==========================================
def create_conversation(email: str, title: str = None):
    db = Session()
    try:
        conversation = Conversation()
        conversation.email = email
        conversation.title = title if title and title.strip() else "New chat"
        conversation.is_deleted = False

        cr.save(conversation, db)

        return {
            "status": 200,
            "message": "Conversation created",
            "data": to_dict(conversation)
        }
    finally:
        db.close()

# ==========================================
# GET USER CONVERSATIONS (LIST)
# ==========================================
def get_user_conversations(email: str):
    db = Session()
    try:
        conversations = cr.find_all_by_email(email, db)
        data = [to_dict(c) for c in conversations]

        return {
            "status": 200,
            "message": "Success",
            "data": data
        }
    finally:
        db.close()

# ==========================================
# GET SINGLE CONVERSATION
# ==========================================
def get_conversation(conversation_id: int, email: str):
    db = Session()
    try:
        conversation = cr.find_by_id_and_email(conversation_id, email, db)
        if not conversation:
            return {
                "status": 404,
                "message": "Conversation not found",
                "data": None
            }

        return {
            "status": 200,
            "message": "Success",
            "data": to_dict(conversation)
        }
    finally:
        db.close()

# ==========================================
# RENAME CONVERSATION
# ==========================================
def rename_conversation(conversation_id: int, new_title: str, email: str):
    db = Session()
    try:
        conversation = cr.find_by_id_and_email(conversation_id, email, db)
        if not conversation:
            return {
                "status": 404,
                "message": "Conversation not found",
                "data": None
            }

        conversation.title = new_title if new_title and new_title.strip() else "Untitled"
        conversation.last_active_at = datetime.now()

        cr.save(conversation, db)

        return {
            "status": 200,
            "message": "Renamed",
            "data": to_dict(conversation)
        }
    finally:
        db.close()

# ==========================================
# SOFT DELETE CONVERSATION
# ==========================================
def delete_conversation(conversation_id: int, email: str):
    db = Session()
    try:
        conversation = cr.find_by_id_and_email(conversation_id, email, db)
        if not conversation:
            return {
                "status": 404,
                "message": "Conversation not found",
                "data": None
            }

        conversation.is_deleted = True
        conversation.deleted_at = datetime.now()

        cr.save(conversation, db)

        return {
            "status": 200,
            "message": "Deleted",
            "data": None
        }
    finally:
        db.close()

# ==========================================
# TOUCH CONVERSATION (TIMESTAMP UPDATE)
# ==========================================
def touch_conversation(conversation_id: int, db):
    conversation = db.get(Conversation, conversation_id)
    if conversation:
        conversation.last_active_at = datetime.now()
        cr.save(conversation, db)
