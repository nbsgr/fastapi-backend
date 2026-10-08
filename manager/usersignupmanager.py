#usersignupmanager.py
from pwdlib import PasswordHash
from dto.signuprequest import SignupRequest
from dto.verifyotprequest import VerifyOtpRequest
from manager import otpmanager as om
from manager import emailmanager as em
from repository import redisrepository as rr

# ==========================================
# PASSWORD HASHER
# ==========================================
password_hash = PasswordHash.recommended()

# ==========================================
# CONSTANTS
# ==========================================
OTP_EXPIRY_TIME = 5
BLOCKED_TIME = 5

# ==========================================
# REQUEST SIGNUP OTP
# ==========================================
def request_signup_otp(request: SignupRequest):
    email = request.email
    username = request.username
    password = request.password

    # Check Request Attempts
    if om.is_attempt_limit_exceeded(email):
        return {
            "status": 400,
            "message": "OTP request attempts exhausted. Try again after",
            "data": om.get_blocked_time_left(email)
        }

    # Generate OTP
    otp = om.generate_otp()

    # Hash Password
    request.password = password_hash.hash(password)

    # Redis Keys
    otp_key = f"signup:otp:{email}"
    data_key = f"signup:data:{email}"
    attempt_key = f"signup:attempt:{email}"

    # Store OTP
    rr.set_with_ttl(
        otp_key,
        otp,
        OTP_EXPIRY_TIME
    )

    # Store Signup Data
    rr.set_with_ttl(
        data_key,
        request.model_dump_json(),
        OTP_EXPIRY_TIME
    )

    # Increment Attempts
    attempts = rr.increment(attempt_key)

    # First Attempt
    if attempts == 1:
        rr.set_ttl(
            attempt_key,
            BLOCKED_TIME
        )

    # Send Email
    email_sent = em.send_otp_email(
        email,
        username,
        otp
    )

    if not email_sent:
        rr.delete(otp_key)
        rr.delete(data_key)
        rr.delete(attempt_key)

        return {
            "status": 500,
            "message": "Unable to send OTP currently",
            "data": None
        }

    return {
        "status": 200,
        "message": "OTP sent successfully",
        "data": om.get_attempts_left(email)
    }

# ==========================================
# VERIFY SIGNUP OTP
# ==========================================
def verify_signup_otp(request: VerifyOtpRequest):
    email = request.email
    otp = request.otp

    otp_key = f"signup:otp:{email}"
    data_key = f"signup:data:{email}"
    attempt_key = f"signup:attempt:{email}"

    # Read Stored OTP
    stored_otp = rr.get_value(otp_key)
    if stored_otp is None:
        return {
            "status": 400,
            "message": "OTP Expired or Invalid",
            "data": om.get_blocked_time_left(email)
        }

    # Compare OTP
    if stored_otp != otp:
        return {
            "status": 400,
            "message": "Invalid OTP",
            "data": None
        }

    # Read Signup Data
    signup_data = rr.get_value(data_key)
    if signup_data is None:
        return {
            "status": 400,
            "message": "Signup session Expired",
            "data": None
        }

    # Convert JSON -> SignUpRequest
    signup_request = SignupRequest.model_validate_json(signup_data)

    # Delete Redis Data
    rr.delete(otp_key)
    rr.delete(data_key)
    rr.delete(attempt_key)

    return {
        "status": 200,
        "message": "OTP verified successfully",
        "data": signup_request
    }
