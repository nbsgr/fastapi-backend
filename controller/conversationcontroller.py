#conversationcontroller.py
from fastapi import APIRouter, Request
from dto.createconversationrequest import CreateConversationRequest
from dto.renameconversationrequest import RenameConversationRequest
from manager import conversationmanager as cm

# ==========================================
# ROUTER
# ==========================================
router = APIRouter(
    prefix="/conversations",
    tags=["Conversations"]
)

# ==========================================
# CREATE CONVERSATION
# ==========================================
@router.post("/create")
def create_conversation(request: Request, body: CreateConversationRequest = None):
    email = request.state.user["email"]
    title = body.title if body else None
    return cm.create_conversation(email, title)

# ==========================================
# GET ALL CONVERSATIONS
# ==========================================
@router.get("/list")
def get_user_conversations(request: Request):
    email = request.state.user["email"]
    return cm.get_user_conversations(email)

# ==========================================
# GET SINGLE CONVERSATION
# ==========================================
@router.get("/{id}")
def get_conversation(id: int, request: Request):
    email = request.state.user["email"]
    return cm.get_conversation(id, email)

# ==========================================
# RENAME CONVERSATION
# ==========================================
@router.put("/rename/{id}")
def rename_conversation(id: int, body: RenameConversationRequest, request: Request):
    email = request.state.user["email"]
    return cm.rename_conversation(id, body.title, email)

# ==========================================
# DELETE CONVERSATION (SOFT DELETE)
# ==========================================
@router.delete("/{id}")
def delete_conversation(id: int, request: Request):
    email = request.state.user["email"]
    return cm.delete_conversation(id, email)
