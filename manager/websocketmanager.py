#websocketmanager.py
from fastapi import WebSocket

# ==========================================
# ACTIVE CONNECTIONS STORAGE
# ==========================================
# email -> WebSocket
active_connections = {}

# ==========================================
# CONNECT
# ==========================================
async def connect(email: str, websocket: WebSocket):
    await websocket.accept()
    active_connections[email] = websocket
    print(f"[WebSocket] Connected: {email}")

# ==========================================
# DISCONNECT
# ==========================================
def disconnect(email: str):
    if email in active_connections:
        del active_connections[email]
        print(f"[WebSocket] Disconnected: {email}")

# ==========================================
# SEND TO USER (UNICAST)
# ==========================================
async def send_to_user(email: str, message: str):
    ws = active_connections.get(email)
    if ws:
        await ws.send_text(message)

# ==========================================
# BROADCAST
# ==========================================
async def broadcast(message: str):
    for email, ws in list(active_connections.items()):
        try:
            await ws.send_text(message)
        except Exception:
            pass
