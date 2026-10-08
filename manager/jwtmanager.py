import os
from datetime import datetime,timedelta,timezone
from jose import jwt,JWTError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#Algorithm
ALGORITHM=os.getenv("ALGORITHM", "HS256")
#jwt secret key
JWT_SECRET = os.getenv("JWT_SECRET", "fallback-secret-key-change-in-env")
#expiration #24hrs
TOKEN_EXPIRY=int(os.getenv("TOKEN_EXPIRY", "24"))

#generate token
def generate_token(user):
    payload={
        "sub":user.email,
        "id":user.id,
        "username":user.username,
        "role":user.role,
        "iat":datetime.now(timezone.utc),
        "exp":datetime.now(timezone.utc)+timedelta(hours=TOKEN_EXPIRY)
    }
    return jwt.encode(payload,JWT_SECRET,algorithm=ALGORITHM)

#Extract al claims
def extract_all_claims(token):
    try:
        return jwt.decode(token,JWT_SECRET,algorithms=[ALGORITHM])
    except JWTError as e:
        print("JWT ERROR:",e)
        return None

#Get Email
def get_email(token):
    claims = extract_all_claims(token)
    if claims is None:
        return None
    return claims.get("sub")

#Get Username
def get_username(token):
    claims = extract_all_claims(token)
    if claims is None:
        return None
    return claims.get("username")

#Get Role
def get_role(token):
    claims = extract_all_claims(token)
    if claims is None:
        return None
    return claims.get("role")

#Get ID
def get_id(token):
    claims = extract_all_claims(token)
    if claims is None:
        return None
    return claims.get("id")

#Get Expiration
def get_expiration(token):
    claims = extract_all_claims(token)
    if claims is None:
        return None
    return claims.get("exp")

#Token Expired
def is_token_expired(token):
    claims = extract_all_claims(token)
    if claims is None:
        return True
    exp=claims.get("exp")
    expiration=datetime.fromtimestamp(exp,tz=timezone.utc)
    return expiration<datetime.now(timezone.utc)

#Token Valid?
def is_token_valid(token):
    claims = extract_all_claims(token)
    if claims is None:
        return False
    else:
        return True



