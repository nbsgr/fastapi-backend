#usermanager.py
from base import Session
from model.user import User
from repository import usersrepository as ur
from manager import usersignupmanager as usm
from manager import userloginmanager as ulm
from manager import passwordresetmanager as prm
from manager import jwtmanager as jm

# ==========================================
# REQUEST SIGNUP OTP
# ==========================================
def request_signup_otp(request):
    db = Session()
    try:
        email = request.email
        username = request.username

        # Check Email Exists
        if ur.exists_by_email(email, db):
            return {
                "status": 400,
                "message": "Email already exists",
                "data": None
            }

        # Check Username Exists
        if ur.exists_by_username(username, db):
            return {
                "status": 400,
                "message": "Username already exists",
                "data": None
            }

        return usm.request_signup_otp(request)

    finally:
        db.close()

# ==========================================
# VERIFY SIGNUP OTP
# ==========================================
def verify_signup_otp(request):
    db = Session()
    try:
        response = usm.verify_signup_otp(request)

        if response["status"] != 200:
            return response

        signup_request = response["data"]

        user = User()
        user.email = signup_request.email
        user.username = signup_request.username
        user.password = signup_request.password

        # 1 = Admin, 2 = User
        user.role = 2

        # 1 = Active, 2 = Blocked
        user.status = 1

        ur.save(user, db)

        return {
            "status": 200,
            "message": "Signup Successful",
            "data": None
        }

    finally:
        db.close()

# ==========================================
# LOGIN
# ==========================================
def login(request):
    response = ulm.login(request)

    if response["status"] != 200:
        return response

    user = response["data"]
    token = jm.generate_token(user)

    return {
        "status": 200,
        "message": "Login Successful",
        "data": {
            "token": token
        }
    }

# ==========================================
# REQUEST PASSWORD RESET
# ==========================================
def request_password_reset(request):
    return prm.request_password_reset(request)

# ==========================================
# RESET PASSWORD
# ==========================================
def reset_password(request):
    return prm.reset_password(request)

# ==========================================
# GET USERNAME
# ==========================================
def get_username(token):
    username = jm.get_username(token)

    if username is None:
        return {
            "status": 401,
            "message": "Token Expired or Invalid",
            "data": None
        }

    return {
        "status": 200,
        "message": "Success",
        "data": username
    }

# ==========================================
# VALIDATE TOKEN
# ==========================================
def validate_token(token):
    if not jm.is_token_valid(token):
        return {
            "status": 401,
            "message": "Token Invalid or Expired",
            "data": None
        }

    return {
        "status": 200,
        "message": "Token Valid",
        "data": {
            "email": jm.get_email(token),
            "username": jm.get_username(token),
            "valid": True
        }
    }
