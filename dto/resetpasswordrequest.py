#restpasswordrequest
from typing import Annotated
from pydantic import BaseModel,EmailStr,Field

class ResetPasswordRequest(BaseModel):

    #Email
    email: EmailStr

    #resetToken
    token: Annotated[
        str,
        Field(
            min_length=1,
        )
    ]

    #New Password
    password: Annotated[
        str,
        Field(
            min_length=1,
            max_length=64
        )
    ]
