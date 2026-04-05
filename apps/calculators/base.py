"""
Base abstract class for all gematria calculators.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any
import logging

logger = logging.getLogger(__name__)


class GematriaCalculator(ABC):
    """
    Abstract base class for all gematria calculators.
    
    Each calculator must implement the calculate() method and define
    a unique name and description.
    """
    
    name: str = "base_calculator"
    description: str = "Base gematria calculator"
    
    def __init__(self):
        """Initialize the calculator."""
        pass
    
    @abstractmethod
    def calculate(self, text: str) -> int:
        """
        Calculate the gematria value for the given text.
        
        Args:
            text: Input text to calculate gematria value for
            
        Returns:
            Integer gematria value
        """
        pass
    
    def clean_text(self, text: str) -> str:
        """
        Remove non-alphabetic characters and convert to lowercase.
        
        Args:
            text: Input text to clean
            
        Returns:
            Cleaned text containing only lowercase letters
        """
        return ''.join(c for c in text if c.isalpha()).lower()
    
    def reduce_to_single_digit(self, value: int) -> int:
        """
        Reduce a number to a single digit by summing its digits repeatedly.
        Example: 26 → 2+6 → 8, 123 → 1+2+3 → 6
        
        Args:
            value: Number to reduce
            
        Returns:
            Single digit (1-9)
        """
        while value > 9:
            value = sum(int(digit) for digit in str(value))
        return value
    
    def get_info(self) -> Dict[str, Any]:
        """
        Get information about this calculator.
        
        Returns:
            Dictionary with calculator name and description
        """
        return {
            'name': self.name,
            'description': self.description,
            'class': self.__class__.__name__,
        }
    
    def __str__(self) -> str:
        """String representation of the calculator."""
        return f"{self.__class__.__name__}(name='{self.name}')"
    
    def __repr__(self) -> str:
        """Developer representation of the calculator."""
        return self.__str__()
