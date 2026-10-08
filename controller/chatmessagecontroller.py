#chatmessagecontroller.py
from fastapi import APIRouter, Request
from dto.sendmessagerequest import SendMessageRequest
from dto.getmessagesrequest import GetMessagesRequest
from manager import chatmessagemanager as cmm

# ==========================================
# ROUTER
# ==========================================
router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

# ==========================================
# REST: SEND USER MESSAGE
# ==========================================
@router.post("/send")
def send_user_message(request: Request, body: SendMessageRequest):
    email = request.state.user["email"]
    return cmm.send_user_message(body.conversation_id, body.content, email)

# ==========================================
# REST: GET CHAT HISTORY
# ==========================================
@router.post("/list")
def get_messages(request: Request, body: GetMessagesRequest):
    email = request.state.user["email"]
    return cmm.get_messages(body.conversation_id, email)
