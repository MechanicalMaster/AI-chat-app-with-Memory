from pydantic import BaseModel
from typing import List, Optional

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    response: str
    history: Optional[List[Message]] = None

class PasswordRequest(BaseModel):
    password: str 