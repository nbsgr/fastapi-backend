#corsconfig.py
from fastapi.middleware.cors import CORSMiddleware

#CORS Configuration
def cors_config(app):
    app.add_middleware(
        CORSMiddleware,

        #Allow Frontend Origin
        allow_origins=["*"],

        #Allow HTTP methods
        allow_methods=["GET", "POST", "OPTIONS","PUT", "DELETE","PATCH"],

        #Allow Headers
        allow_headers=["*"],

        #Allow Credentials False because jwt
        allow_credentials=False,
    )