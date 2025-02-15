import logging
from datetime import datetime
import os

class Logger:
    def __init__(self):
        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        # Set up logging
        self.logger = logging.getLogger('chat_app')
        self.logger.setLevel(logging.INFO)

        # Create file handler
        log_file = f'logs/chat_{datetime.now().strftime("%Y%m%d")}.log'
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Create formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add handlers to logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_chat(self, session_id: str, user_input: str, response: str):
        """Log chat interactions"""
        self.logger.info(f"Session: {session_id}")
        self.logger.info(f"User: {user_input}")
        self.logger.info(f"Assistant: {response}")
        self.logger.info("-" * 50)

    def log_error(self, session_id: str, error: str):
        """Log errors"""
        self.logger.error(f"Session: {session_id}")
        self.logger.error(f"Error: {error}")
        self.logger.error("-" * 50)

logger = Logger() 