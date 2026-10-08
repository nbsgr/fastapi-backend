#otpmanager.py
import random
from repository import redisrepository as rr

# ==========================================
# CONSTANTS
# ==========================================

# Maximum OTP Requests
MAX_ATTEMPTS = 5

# OTP Expiry Time (Minutes)
OTP_EXPIRY_TIME = 5

# Block Time (Minutes)
BLOCKED_TIME = 5

# ==========================================
# GENERATE OTP
# ==========================================
def generate_otp():
    return str(random.randint(100000, 999999))

# ==========================================
# CHECK ATTEMPT LIMIT
# ==========================================
def is_attempt_limit_exceeded(email):
    key = f"signup:attempt:{email}"
    value = rr.get_value(key)
    if value is None:
        return False
    attempts = int(value)
    return attempts >= MAX_ATTEMPTS

# ==========================================
# GET ATTEMPTS LEFT
# ==========================================
def get_attempts_left(email):
    key = f"signup:attempt:{email}"
    value = rr.get_value(key)
    if value is None:
        return MAX_ATTEMPTS
    attempts = int(value)
    return MAX_ATTEMPTS - attempts

# ==========================================
# GET BLOCKED TIME LEFT
# ==========================================
def get_blocked_time_left(email):
    key = f"signup:attempt:{email}"
    return rr.get_ttl(key)
