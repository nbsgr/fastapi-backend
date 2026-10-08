#loginrequest.py
from typing import Annotated
from pydantic import BaseModel,Field

class LoginRequest(BaseModel):

    #Email or Username
    emailorusername: Annotated[
        str,
        Field(
            min_length=1
        )
    ]

    password: Annotated[
        str,
        Field(
            min_length=1
        )
    ]