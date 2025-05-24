from fastapi import APIRouter
from services.chat_service import ChatService
from schemas.chat_schema import ChatMessage
chat_router = APIRouter()
chat_service = ChatService()

@chat_router.post("/new/message/")
def post_message(message: ChatMessage):
    return chat_service.post_message(message)

@chat_router.get("/get/messages/")
def get_messages():
    return chat_service.get_messages()
