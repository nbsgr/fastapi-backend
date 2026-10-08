#userloginattemptsmanager.py
from repository import redisrepository as rr

# ==========================================
# CONSTANTS
# ==========================================
MAX_LOGIN_ATTEMPTS = 5
BLOCKED_TIME = 5

# ==========================================
# IS ATTEMPT LIMIT EXCEEDED
# ==========================================
def is_attempt_limit_exceeded(emailorusername):
    key = f"login:attempt:{emailorusername}"
    value = rr.get_value(key)
    if value is None:
        return False
    attempts = int(value)
    return attempts >= MAX_LOGIN_ATTEMPTS

# ==========================================
# GET ATTEMPTS LEFT
# ==========================================
def get_attempts_left(emailorusername):
    key = f"login:attempt:{emailorusername}"
    value = rr.get_value(key)
    if value is None:
        return MAX_LOGIN_ATTEMPTS
    attempts = int(value)
    return MAX_LOGIN_ATTEMPTS - attempts

# ==========================================
# GET BLOCKED TIME LEFT
# ==========================================
def get_blocked_time_left(emailorusername):
    key = f"login:attempt:{emailorusername}"
    return rr.get_ttl(key)
