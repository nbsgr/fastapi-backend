#renameconversationrequest.py
from typing import Annotated
from pydantic import BaseModel, Field

class RenameConversationRequest(BaseModel):
    title: Annotated[
        str,
        Field(
            min_length=1,
            max_length=255
        )
    ]
