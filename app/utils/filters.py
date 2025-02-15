import re
from typing import Tuple

class InputOutputFilter:
    def __init__(self):
        self.blocked_patterns = [
            r'(?i)(hack|crack|exploit)',
            r'(?i)(password|credentials)',
            r'(?i)(private|confidential)\s+data',
        ]

        self.required_patterns = [
            r'(?i)(loan|finance|credit|banking|document)',
        ]

    def filter_input(self, text: str) -> Tuple[bool, str]:
        """
        Filter input text
        Returns: (is_safe, filtered_text)
        """
        # Check for blocked patterns
        for pattern in self.blocked_patterns:
            if re.search(pattern, text):
                return False, "I cannot process requests related to security or private information."

        # Check if text is related to banking/loans
        has_required = any(re.search(pattern, text) for pattern in self.required_patterns)
        if not has_required:
            return False, "Please ask questions related to loans and banking services."

        # Sanitize input
        filtered_text = re.sub(r'[^\w\s.,?!-]', '', text)
        return True, filtered_text

    def filter_output(self, text: str) -> str:
        """Filter output text to ensure compliance"""
        # Remove any potential sensitive information
        text = re.sub(r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b', '[CARD NUMBER REMOVED]', text)
        text = re.sub(r'\b\d{9,}\b', '[ID REMOVED]', text)
        
        return text

input_output_filter = InputOutputFilter() 