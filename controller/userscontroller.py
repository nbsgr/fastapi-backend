#userscontroller.py
from fastapi import APIRouter, Request

from dto.signuprequest import SignupRequest
from dto.verifyotprequest import VerifyOtpRequest
from dto.loginrequest import LoginRequest
from dto.forgotpasswordrequest import ForgotPasswordRequest
from dto.resetpasswordrequest import ResetPasswordRequest

from manager import usermanager as um

# ==========================================
# ROUTER
# ==========================================
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# ==========================================
# REQUEST SIGNUP OTP
# ==========================================
@router.post("/signup/request-otp")
def request_signup_otp(request: SignupRequest):
    return um.request_signup_otp(request)

# ==========================================
# VERIFY SIGNUP OTP
# ==========================================
@router.post("/signup/verify-otp")
def verify_signup_otp(request: VerifyOtpRequest):
    return um.verify_signup_otp(request)

# ==========================================
# LOGIN
# ==========================================
@router.post("/login")
def login(request: LoginRequest):
    return um.login(request)

# ==========================================
# FORGOT PASSWORD
# ==========================================
@router.post("/forgot-password")
def forgot_password(request: ForgotPasswordRequest):
    return um.request_password_reset(request)

# ==========================================
# RESET PASSWORD
# ==========================================
@router.post("/reset-password")
def reset_password(request: ResetPasswordRequest):
    return um.reset_password(request)

# ==========================================
# CURRENT USER
# ==========================================
@router.get("/me")
def me(request: Request):
    return {
        "status": 200,
        "message": "Success",
        "data": request.state.user["username"]
    }