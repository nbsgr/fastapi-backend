#chatwebsocketcontroller.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Query, status
from manager import jwtmanager as jm
from manager import websocketmanager as wm
from manager import chatstreammanager as csm

router = APIRouter(
    tags=["WebSocket"]
)

# ==========================================
# WEBSOCKET: /ws/chat
# ==========================================
@router.websocket("/ws/chat")
async def chat_websocket(
    websocket: WebSocket,
    token: str = Query(...)
):
    # ------------------------------------------
    # 1. AUTHENTICATE DURING HANDSHAKE
    # ------------------------------------------
    if not jm.is_token_valid(token):
        print("[WebSocket Auth] Rejected: Invalid Token")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    email = jm.get_email(token)
    if not email:
        print("[WebSocket Auth] Rejected: No email in claims")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # ------------------------------------------
    # 2. ACCEPT CONNECTION
    # ------------------------------------------
    await wm.connect(email, websocket)

    try:
        # ------------------------------------------
        # 3. LISTEN FOR INCOMING MESSAGES
        # ------------------------------------------
        while True:
            data = await websocket.receive_json()
            print(f"[WebSocket Received] Payload: {data}")

            conversation_id = data.get("conversation_id") or data.get("conversationId")
            user_message = data.get("content")

            if not conversation_id or not user_message:
                await websocket.send_json({"error": "Invalid payload. 'conversation_id' and 'content' required."})
                continue

            # ------------------------------------------
            # 4. TRIGGER AI STREAMING
            # ------------------------------------------
            print(f"[WebSocket Triggering Stream] conv_id: {conversation_id}, user: {email}")
            await csm.stream_bot_reply(
                conversation_id=int(conversation_id),
                user_message=user_message,
                email=email,
                websocket=websocket
            )

    except WebSocketDisconnect:
        wm.disconnect(email)
    except Exception as e:
        print(f"[WebSocket Error] {e}")
        wm.disconnect(email)
