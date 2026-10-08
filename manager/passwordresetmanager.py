#passwordresetmanager.py
import secrets
from pwdlib import PasswordHash
from base import Session
from dto.forgotpasswordrequest import ForgotPasswordRequest
from dto.resetpasswordrequest import ResetPasswordRequest
from manager import emailmanager as em
from repository import usersrepository as ur
from repository import redisrepository as rr

# ==========================================
# PASSWORD HASHER
# ==========================================
password_hash = PasswordHash.recommended()

# ==========================================
# CONSTANTS
# ==========================================
RESET_TOKEN_EXPIRY = 10
MAX_RESET_ATTEMPTS = 5
RESET_BLOCK_TIME = 30

# ==========================================
# REQUEST PASSWORD RESET
# ==========================================
def request_password_reset(request: ForgotPasswordRequest):
    db = Session()
    try:
        email = request.email

        # Find User
        user = ur.find_by_email(email, db)

        # Don't reveal whether email exists
        if user is None:
            return {
                "status": 200,
                "message": "If the email exists, a reset link has been sent",
                "data": None
            }

        block_key = f"reset:block:{email}"

        # Check Block
        if rr.exists(block_key):
            return {
                "status": 403,
                "message": "Too many reset attempts. Try again after",
                "data": rr.get_ttl(block_key)
            }

        token_key = f"reset:token:{email}"

        # Delete Old Token
        rr.delete(token_key)

        # Generate Reset Token
        reset_token = secrets.token_hex(32)

        # Store Token
        rr.set_with_ttl(
            token_key,
            reset_token,
            RESET_TOKEN_EXPIRY
        )

        # Send Email
        email_sent = em.send_password_reset_email(
            email,
            user.username,
            reset_token
        )

        if not email_sent:
            rr.delete(token_key)
            return {
                "status": 500,
                "message": "Failed to send reset email",
                "data": None
            }

        return {
            "status": 200,
            "message": "If the email exists, a reset link has been sent",
            "data": None
        }

    finally:
        db.close()

# ==========================================
# RESET PASSWORD
# ==========================================
def reset_password(request: ResetPasswordRequest):
    db = Session()
    try:
        email = request.email
        token = request.token
        password = request.password

        token_key = f"reset:token:{email}"
        attempt_key = f"reset:attempt:{email}"
        block_key = f"reset:block:{email}"

        # Check Block
        if rr.exists(block_key):
            return {
                "status": 403,
                "message": "Too many failed attempts. Try again after",
                "data": rr.get_ttl(block_key)
            }

        # Get Stored Token
        stored_token = rr.get_value(token_key)
        if stored_token is None:
            return {
                "status": 400,
                "message": "Invalid or Expired Reset Token",
                "data": None
            }

        # Verify Token
        if stored_token != token:
            attempts = rr.increment(attempt_key)

            if attempts == 1:
                rr.set_ttl(
                    attempt_key,
                    RESET_TOKEN_EXPIRY
                )

            if attempts >= MAX_RESET_ATTEMPTS:
                rr.set_with_ttl(
                    block_key,
                    "blocked",
                    RESET_BLOCK_TIME
                )
                rr.delete(token_key)
                rr.delete(attempt_key)

                return {
                    "status": 403,
                    "message": "Too many failed attempts. Try again after",
                    "data": RESET_BLOCK_TIME
                }

            remaining_attempts = MAX_RESET_ATTEMPTS - attempts
            return {
                "status": 400,
                "message": "Invalid Reset Token",
                "data": remaining_attempts
            }

        # Find User
        user = ur.find_by_email(email, db)
        if user is None:
            return {
                "status": 404,
                "message": "User Not Found",
                "data": None
            }

        # Hash Password
        user.password = password_hash.hash(password)

        # Save User
        ur.save(user, db)

        # Cleanup
        rr.delete(token_key)
        rr.delete(attempt_key)
        rr.delete(block_key)

        return {
            "status": 200,
            "message": "Password Reset Successful",
            "data": None
        }

    finally:
        db.close()
