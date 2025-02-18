from fastapi import APIRouter, HTTPException
from app.models.chat import ChatRequest, ChatResponse
from app.services.chat_service import ChatService
from app.core.config import settings

router = APIRouter()
chat_service = ChatService(api_key=settings.OPENAI_API_KEY)

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        response = await chat_service.get_response(request.message, request.session_id)
        return ChatResponse(
            response=response,
            history=[]  # We'll implement history later if needed
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/clear/{session_id}")
async def clear_history(session_id: str):
    try:
        chat_service.memory_service.clear_memory(session_id)
        return {"status": "success", "message": "Chat history cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 