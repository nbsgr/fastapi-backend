#getmessagesrequest.py
from pydantic import BaseModel

class GetMessagesRequest(BaseModel):
    conversation_id: int
