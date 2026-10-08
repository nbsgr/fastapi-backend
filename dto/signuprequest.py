#signupequest.py
from typing import Annotated
from pydantic import EmailStr, BaseModel,Field

class SignupRequest(BaseModel):

    #Email
    email: EmailStr

    #username:
    username:Annotated[
        str,
        Field(
            min_length=1,
            max_length=64,
            pattern=r"^[a-zA-Z0-9_]+$"
        )
    ]

    #pssword
    password:Annotated[
        str,
        Field(
            min_length=1
        )
    ]