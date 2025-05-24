from pydantic import BaseModel, Field

class Message(BaseModel):
    role: str
    content: str

class ChatMessage(BaseModel):
    prompt: str
    max_tokens: int
    temperature: float = Field(default=1.0)
    top_p: float = Field(default=1.0)
    