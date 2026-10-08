#chatmessagemanager.py
import json
from base import Session
from model.chatmessage import ChatMessage
from repository import chatmessagerepository as cmr
from repository import conversationrepository as cr
from manager import conversationmanager as cm

# ==========================================
# SERIALIZER HELPER
# ==========================================
def to_dict(m: ChatMessage):
    if not m:
        return None
    return {
        "id": m.id,
        "conversation_id": m.conversation_id,
        "sender_type": m.sender_type,
        "content": m.content,
        "sent_at": m.sent_at.isoformat() if m.sent_at else None,
        "sources": m.sources,
    }

# ==========================================
# REST: SEND USER MESSAGE
# ==========================================
def send_user_message(conversation_id: int, content: str, email: str):
    db = Session()
    try:
        if not content or not content.strip():
            return {
                "status": 400,
                "message": "Message content is empty",
                "data": None
            }

        # Verify conversation ownership
        conversation = cr.find_by_id_and_email(conversation_id, email, db)
        if not conversation:
            return {
                "status": 404,
                "message": "Conversation not found",
                "data": None
            }

        # Create message
        user_message = ChatMessage(
            conversation_id=conversation_id,
            sender_type="USER",
            content=content.strip(),
            sources=None
        )

        cmr.save(user_message, db)
        cm.touch_conversation(conversation_id, db)

        return {
            "status": 200,
            "message": "Message sent",
            "data": to_dict(user_message)
        }
    finally:
        db.close()

# ==========================================
# REST: GET MESSAGES
# ==========================================
def get_messages(conversation_id: int, email: str):
    db = Session()
    try:
        # Verify conversation ownership
        conversation = cr.find_by_id_and_email(conversation_id, email, db)
        if not conversation:
            return {
                "status": 404,
                "message": "Conversation not found",
                "data": None
            }

        messages = cmr.find_by_conversation_id(conversation_id, db)
        data = [to_dict(m) for m in messages]

        return {
            "status": 200,
            "message": "Success",
            "data": data
        }
    finally:
        db.close()

# ==========================================
# SAVE BOT MESSAGE INTERNAL
# ==========================================
def save_bot_message_internal(conversation_id: int, content: str, sources: list = None, db=None):
    should_close = False
    if db is None:
        db = Session()
        should_close = True

    try:
        sources_json = json.dumps(sources) if sources else None

        bot_message = ChatMessage(
            conversation_id=conversation_id,
            sender_type="BOT",
            content=content.strip() if content else "",
            sources=sources_json
        )

        cmr.save(bot_message, db)
        cm.touch_conversation(conversation_id, db)

        return bot_message
    finally:
        if should_close:
            db.close()
