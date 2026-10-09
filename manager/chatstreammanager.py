import os
import json
import httpx
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from base import Session
from repository import conversationrepository as cr
from repository import chatmessagerepository as cmr
from manager import chatmessagemanager as cmm
from manager import conversationmanager as cm

# ==========================================
# CONFIGURATION
# ==========================================
AI_STREAM_URL = os.getenv("AI_STREAM_URL", "http://localhost:5000/api/process-stream")

# ==========================================
# EXTRACT CLEAN CONTENT FROM NDJSON
# ==========================================
def extract_content_from_ndjson(raw: str):
    if not raw or not raw.strip():
        return ""

    final_text = []
    for line in raw.split("\n"):
        trimmed = line.strip()
        if not trimmed:
            continue
        if not trimmed.startswith("{"):
            final_text.append(trimmed)
            continue
        try:
            node = json.loads(trimmed)
            if "message" in node and "content" in node["message"]:
                final_text.append(node["message"]["content"])
        except Exception:
            pass

    return "".join(final_text).strip()

# ==========================================
# ==========================================
# STREAM BOT REPLY OVER WEBSOCKET
# ==========================================
async def stream_bot_reply(conversation_id: int, user_message: str, email: str, websocket):
    # 1. Verify conversation ownership & fetch context history
    db = Session()
    try:
        conversation = cr.find_by_id_and_email(conversation_id, email, db)
        if not conversation:
            await websocket.send_json({"error": "Conversation not found"})
            return

        history = cmr.find_by_conversation_id(conversation_id, db)
    finally:
        db.close()

    # 2. Format history (up to last 20 messages)
    formatted_messages = []
    if history:
        for msg in history:
            sender = msg.sender_type
            content = msg.content
            if sender == "USER" and content and content.strip():
                formatted_messages.append({
                    "role": "user",
                    "content": content.strip()
                })
            elif sender == "BOT" and content and content.strip():
                clean_bot_text = extract_content_from_ndjson(content)
                if clean_bot_text:
                    formatted_messages.append({
                        "role": "assistant",
                        "content": clean_bot_text
                    })

    # Ensure current message is at end
    if not formatted_messages or formatted_messages[-1].get("content") != user_message.strip():
        formatted_messages.append({
            "role": "user",
            "content": user_message.strip()
        })

    # Keep last 20 messages for context window
    if len(formatted_messages) > 20:
        formatted_messages = formatted_messages[-20:]

    full_answer = []

    # 3. Stream from AI Backend
    payload = {
        "question": user_message,
        "messages": formatted_messages
    }

    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            async with client.stream("POST", AI_STREAM_URL, json=payload) as response:
                async for chunk in response.aiter_text():
                    if chunk and chunk.strip():
                        # Forward immediately to WebSocket client
                        await websocket.send_text(chunk.strip())
                        full_answer.append(chunk.strip())
                        full_answer.append("\n")
    except Exception as e:
        print(f"[ChatStreamManager] AI Stream Error: {e}")
        error_chunk = json.dumps({"error": "AI service unavailable", "detail": str(e)})
        await websocket.send_text(error_chunk)

    # 4. Save Final Bot Message to Database
    if full_answer:
        complete_content = "".join(full_answer).strip()
        cmm.save_bot_message_internal(
            conversation_id=conversation_id,
            content=complete_content,
            sources=None,
            db=None
        )

