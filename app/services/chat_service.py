from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableWithMessageHistory
from app.config import settings
from app.services.memory_service import MemoryService
from app.utils.logger import logger
from app.utils.filters import InputOutputFilter

class ChatService:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            api_key=api_key,
            temperature=0.7,
            model_name="gpt-3.5-turbo"
        )
        
        self.prompt = ChatPromptTemplate.from_messages([
            ("system","You are an expert Indian Banker specializing in Channel Finance (Dealer Finance/Supply Chain Finance). Your goal is to answer questions about Channel Finance to dealers of anchor companies in a clear, short and professional manner"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        self.chain = self.prompt | self.llm | StrOutputParser()
        self.memory_service = MemoryService()
        self.filter = InputOutputFilter()

    async def get_response(self, message: str, session_id: str) -> str:
        """Get response from LLM with enhanced memory and filtering"""
        try:
            # Filter input
            is_safe, filtered_input = self.filter.filter_input(message)
            if not is_safe:
                logger.log_chat(session_id, message, filtered_input)
                return filtered_input

            # Get conversation history
            history = await self.memory_service.get_formatted_history(session_id)
            
            # Generate response
            response = await self.chain.ainvoke({
                "history": history,
                "input": filtered_input
            })

            # Filter output
            filtered_response = self.filter.filter_output(response)

            # Log the interaction
            logger.log_chat(session_id, filtered_input, filtered_response)

            # Save to memory
            self.memory_service.save_context(session_id, filtered_input, filtered_response)

            return filtered_response
            
        except Exception as e:
            error_msg = str(e)
            logger.log_error(session_id, error_msg)
            return "I apologize, but I encountered an error. Please try again."

    def clear_memory(self) -> None:
        """Clear the conversation memory"""
        self.memory_service.clear()

    async def get_response_enhanced(self, user_input: str, session_id: str) -> str:
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