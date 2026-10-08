#verifyotprequest.py
from typing import Annotated
from pydantic import BaseModel,EmailStr,Field

class VerifyOtpRequest(BaseModel):

    #Email
    email:EmailStr

    #otp
    otp:Annotated[
        str,
        Field(
            min_length=1,
            max_length=10,
            pattern=r"^\d{6}$"
        )
    ]