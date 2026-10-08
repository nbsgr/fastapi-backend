#jwtfilter.py
from fastapi import Request
from fastapi.responses import JSONResponse
from manager import jwtmanager as jwt

#public urls
PUBLIC_URLS = [
    "/docs",
    "/openapi.json",
    "/redoc",
    "/users/signup/request-otp",
    "/users/signup/verify-otp",
    "/users/login",
    "/users/forgot-password",
    "/users/reset-password",
    "/ws/chat"
]

#jwt-filter
def jwt_filter(app):
    @app.middleware("http")
    async def middleware(request: Request, call_next):
        #get request path
        path = request.url.path
        method = request.method

        if method == "OPTIONS":
            return await call_next(request)

        #check public urls
        if path in PUBLIC_URLS:
            return await call_next(request)

        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return JSONResponse(
                status_code=401,
                content={
                    "message": "Invalid Authorization Header"
                }
            )

        #extract token
        token=auth_header[7:]

        #validate token
        if not jwt.is_token_valid(token):
            return JSONResponse(
                status_code=401,
                content={
                    "message":"Invalid Token"
                }
            )

        #extract claims
        email=jwt.get_email(token)
        username=jwt.get_username(token)
        role=jwt.get_role(token)
        uid=jwt.get_id(token)

        print("id :", uid, "email: ", email, "username: ", username, "role: ", role)

        #store user details
        request.state.user={
            "id":uid,
            "email":email,
            "username":username,
            "role":role,
        }

        #continue filter chain
        response=await call_next(request)
        return response
