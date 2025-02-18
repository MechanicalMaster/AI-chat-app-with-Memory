from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from app.config import settings
from app.services.memory_service import MemoryService
import re
from app.utils.logger import logger
from app.utils.filters import InputOutputFilter

class ChatService:
    def __init__(self):
        self.llm = ChatOpenAI(
            temperature=settings.TEMPERATURE,
            model_name=settings.MODEL_NAME,
            max_tokens=settings.MAX_TOKENS
        )
        self.memory_service = MemoryService()
        self.filter = InputOutputFilter()

    async def get_response(self, user_input: str, session_id: str) -> str:
        """Get response from LLM with enhanced memory and filtering"""
        try:
            # Filter input
            is_safe, filtered_input = self.filter.filter_input(user_input)
            if not is_safe:
                logger.log_chat(session_id, user_input, filtered_input)
                return filtered_input

            # Get conversation history with summarization
            history = await self.memory_service.get_formatted_history(session_id)
            
            # Create messages for LLM
            messages = [
                SystemMessage(content=settings.SYSTEM_PROMPT),
                HumanMessage(content=f"{history}\nUser: {filtered_input}")
            ]

            # Get response from LLM
            response = await self.llm.agenerate([messages])
            response_text = response.generations[0][0].text

            # Filter output
            filtered_response = self.filter.filter_output(response_text)

            # Log the interaction
            logger.log_chat(session_id, filtered_input, filtered_response)

            # Save to memory
            self.memory_service.save_context(session_id, filtered_input, filtered_response)

            return filtered_response
            
        except Exception as e:
            error_msg = str(e)
            logger.log_error(session_id, error_msg)
            return "I apologize, but I encountered an error. Please try again."

    def is_on_topic(self, response: str, user_input: str) -> bool:
        """Enhanced topic checking - removed as we're relying on the LLM's system prompt"""
        return True  # Let the LLM handle topic enforcement via system prompt 