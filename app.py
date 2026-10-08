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

# Register Routers
app.include_router(users_router)
app.include_router(conversations_router)
app.include_router(messages_router)
app.include_router(websocket_router)

# Import models to ensure table creation
from model.user import User
from model.conversation import Conversation
from model.chatmessage import ChatMessage

# Create tables
Base.metadata.create_all(bind=engine)

# Start server
if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )