from typing import Dict, List, Tuple
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

class MemoryService:
    def __init__(self):
        self.memory: Dict[str, List[Tuple[str, str]]] = {}
        self.summarizer = ChatOpenAI(
            temperature=0,
            model_name="gpt-3.5-turbo"
        )

    def save_context(self, session_id: str, user_input: str, ai_response: str) -> None:
        """Save the conversation context"""
        if session_id not in self.memory:
            self.memory[session_id] = []
        self.memory[session_id].append((user_input, ai_response))

    async def get_formatted_history(self, session_id: str) -> List[dict]:
        """Get formatted conversation history"""
        if session_id not in self.memory:
            return []
        
        messages = []
        for user_msg, ai_msg in self.memory[session_id]:
            messages.append(HumanMessage(content=user_msg))
            messages.append(AIMessage(content=ai_msg))
        return messages

    def clear_memory(self, session_id: str) -> None:
        """Clear the conversation memory for a session"""
        if session_id in self.memory:
            self.memory[session_id] = [] 