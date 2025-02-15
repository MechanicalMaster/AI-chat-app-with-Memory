from typing import List, Dict
from app.models.chat import Message
from app.config import settings
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage

class MemoryService:
    def __init__(self):
        self.sessions: Dict[str, List[Message]] = {}
        self.summarizer = ChatOpenAI(
            temperature=0.3,
            model_name=settings.MODEL_NAME
        )

    def load_memory(self, session_id: str) -> List[Message]:
        """Load conversation history for a session"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
        return self.sessions[session_id]

    def save_context(self, session_id: str, user_input: str, llm_response: str):
        """Save new messages to conversation history"""
        if session_id not in self.sessions:
            self.sessions[session_id] = []
            
        self.sessions[session_id].extend([
            Message(role="user", content=user_input),
            Message(role="assistant", content=llm_response)
        ])
        
        # Apply sliding window if needed
        if len(self.sessions[session_id]) > settings.WINDOW_SIZE * 2:
            self.sessions[session_id] = self.sessions[session_id][-settings.WINDOW_SIZE * 2:]

    def clear_memory(self, session_id: str):
        """Clear conversation history for a session"""
        self.sessions[session_id] = []

    async def summarize_history(self, history: List[Message]) -> str:
        """Summarize conversation history"""
        if len(history) < 10:  # Don't summarize short conversations
            return ""
            
        history_text = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
        messages = [
            SystemMessage(content="Summarize the key points of this conversation about bank loans. Be concise."),
            HumanMessage(content=history_text)
        ]
        
        response = await self.summarizer.agenerate([messages])
        return response.generations[0][0].text

    async def get_formatted_history(self, session_id: str) -> str:
        """Get formatted history with summarization for long conversations"""
        history = self.load_memory(session_id)
        
        if len(history) > settings.WINDOW_SIZE * 2:
            # Summarize older messages
            older_messages = history[:-settings.WINDOW_SIZE * 2]
            summary = await self.summarize_history(older_messages)
            
            # Get recent messages
            recent_messages = history[-settings.WINDOW_SIZE * 2:]
            formatted = f"Previous conversation summary: {summary}\n\nRecent messages:\n"
            formatted += "\n".join([f"{msg.role}: {msg.content}" for msg in recent_messages])
        else:
            formatted = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
            
        return formatted 