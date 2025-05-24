from schemas.chat_schema import ChatMessage

class ChatService:
    def post_message(self, message: ChatMessage) :
        print(message.prompt)
        return {"message": "post message"}
    def get_messages(self):
        return {"message": "get message"}
