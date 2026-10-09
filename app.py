#app.py
from fastapi import FastAPI
import uvicorn

# Database starts
from base import Base, engine

# Middleware imports
from config.corsconfig import cors_config
from config.jwtfilter import jwt_filter

# Controller imports
from controller.userscontroller import router as users_router
from controller.conversationcontroller import router as conversations_router
from controller.chatmessagecontroller import router as messages_router
from controller.chatwebsocketcontroller import router as websocket_router

# FastAPI application
app = FastAPI()
cors_config(app)
jwt_filter(app)

# Root endpoint
@app.get("/")
def read_root():
    return {
        "status": 200,
        "message": "FastAPI Backend is running successfully!",
        "data": None
    }

# Diagnostics endpoint to check DB and Redis on Vercel
@app.get("/api/health-check")
def health_check():
    from sqlalchemy import text
    from repository import redisrepository as rr
    results = {}
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        results["database"] = "CONNECTED"
    except Exception as e:
        results["database"] = f"ERROR: {str(e)}"

    try:
        rr.redis.ping()
        results["redis"] = "CONNECTED"
    except Exception as e:
        results["redis"] = f"ERROR: {str(e)}"

    import os
    brevo_key = os.getenv("BREVO_API_KEY", "")
    brevo_sender = os.getenv("BREVO_SENDER_EMAIL", "")
    results["brevo"] = {
        "api_key_set": bool(brevo_key),
        "api_key_len": len(brevo_key),
        "sender_email": brevo_sender
    }

    return {
        "status": 200,
        "message": "Health Check",
        "data": results
    }

# Register Routers
app.include_router(users_router)
app.include_router(conversations_router)
app.include_router(messages_router)
app.include_router(websocket_router)

# Import models to ensure table creation
from model.user import User
from model.conversation import Conversation
from model.chatmessage import ChatMessage

# Safely ensure tables exist
try:
    Base.metadata.create_all(bind=engine)
except Exception as e:
    print(f"[Database Init Warning] {e}")

# Start server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )