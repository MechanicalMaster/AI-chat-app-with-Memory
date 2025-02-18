import re
from typing import Tuple

class InputOutputFilter:
    def filter_input(self, text: str) -> Tuple[bool, str]:
        """Filter user input
        Returns: (is_safe, filtered_text)
        """
        # Add any input filtering logic here
        if not text.strip():
            return False, "Please provide a valid message."
        
        # Check if the message is loan/finance related
        finance_keywords = ['loan', 'finance', 'bank', 'credit', 'mortgage', 'interest', 'payment', 'debt', 'money']
        if not any(keyword in text.lower() for keyword in finance_keywords):
            return False, "Please ask questions related to loans and banking services."
            
        return True, text

    def filter_output(self, text: str) -> str:
        """Filter assistant output"""
        # Add any output filtering logic here
        return text

input_output_filter = InputOutputFilter() 