#forgotpasswordrequest.py
from pydantic import BaseModel,EmailStr

class ForgotPasswordRequest(BaseModel):

    #Email
    email: EmailStr