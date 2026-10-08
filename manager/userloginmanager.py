#userloginmanager.py
from pwdlib import PasswordHash
from base import Session
from dto.loginrequest import LoginRequest
from repository import usersrepository as ur
from repository import redisrepository as rr
from manager import userloginattemptsmanager as ulam

# ==========================================
# PASSWORD HASHER
# ==========================================
password_hash = PasswordHash.recommended()

# ==========================================
# CONSTANTS
# ==========================================
MAX_LOGIN_ATTEMPTS = 5
BLOCKED_TIME = 5

# ==========================================
# LOGIN
# ==========================================
def login(request: LoginRequest):
    db = Session()
    try:
        emailorusername = request.emailorusername
        password = request.password

        # --------------------------------------
        # CHECK LOGIN ATTEMPTS
        # --------------------------------------
        if ulam.is_attempt_limit_exceeded(emailorusername):
            return {
                "status": 403,
                "message": "Too many failed login attempts. Try again after",
                "data": ulam.get_blocked_time_left(emailorusername)
            }

        # --------------------------------------
        # FIND USER
        # --------------------------------------
        user = ur.find_by_email_or_username(
            emailorusername,
            emailorusername,
            db
        )

        if user is None:
            return failed_login_attempt(emailorusername)

        # --------------------------------------
        # ACCOUNT BLOCKED
        # --------------------------------------
        if user.status == 2:
            return {
                "status": 403,
                "message": "Account blocked by Admin",
                "data": None
            }

        # --------------------------------------
        # VERIFY PASSWORD
        # --------------------------------------
        if not password_hash.verify(password, user.password):
            return failed_login_attempt(emailorusername)

        # --------------------------------------
        # CLEAR LOGIN ATTEMPTS
        # --------------------------------------
        rr.delete(f"login:attempt:{emailorusername}")

        return {
            "status": 200,
            "message": "Login Successful",
            "data": user
        }

    finally:
        db.close()

# ==========================================
# FAILED LOGIN
# ==========================================
def failed_login_attempt(emailorusername):
    attempt_key = f"login:attempt:{emailorusername}"
    attempts = rr.increment(attempt_key)

    if attempts == 1:
        rr.set_ttl(
            attempt_key,
            BLOCKED_TIME
        )

    if ulam.is_attempt_limit_exceeded(emailorusername):
        return {
            "status": 403,
            "message": "Too many failed login attempts. Try again after",
            "data": ulam.get_blocked_time_left(emailorusername)
        }

    return {
        "status": 400,
        "message": "Login Failed",
        "data": ulam.get_attempts_left(emailorusername)
    }
