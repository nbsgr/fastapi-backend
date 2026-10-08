#sendmessagerequest.py
from typing import Annotated
from pydantic import BaseModel, Field

class SendMessageRequest(BaseModel):
    conversation_id: int
    content: Annotated[
        str,
        Field(
            min_length=1
        )
    ]
