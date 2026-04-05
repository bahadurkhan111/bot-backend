"""
Basic gematria calculators: Ordinal, Reduction, Reverse variants.
"""
from .base import GematriaCalculator
import logging

logger = logging.getLogger(__name__)


class OrdinalCalculator(GematriaCalculator):
    """
    Ordinal gematria calculator.
    Maps a=1, b=2, c=3, ..., z=26
    """
    
    name = "ordinal"
    description = "Standard English gematria (a=1, b=2, ..., z=26)"
    
    def calculate(self, text: str) -> int:
        """
        Calculate ordinal value.
        
        Args:
            text: Input text
            
        Returns:
            Sum of ordinal values of all letters
        """
        cleaned = self.clean_text(text)
        total = sum(ord(char) - ord('a') + 1 for char in cleaned)
        logger.debug(f"Ordinal calculation for '{text}': {total}")
        return total


class ReductionCalculator(GematriaCalculator):
    """
    Reduction gematria calculator.
    Calculate ordinal value, then reduce to single digit.
    Example: "hello" → ordinal=52 → 5+2=7
    """
    
    name = "reduction"
    description = "Ordinal value reduced to single digit"
    
    def calculate(self, text: str) -> int:
        """
        Calculate reduction value.
        
        Args:
            text: Input text
            
        Returns:
            Single digit (1-9) after reduction
        """
        cleaned = self.clean_text(text)
        # Calculate ordinal value for each letter and reduce individually
        total = sum(
            self.reduce_to_single_digit(ord(char) - ord('a') + 1)
            for char in cleaned
        )
        # Reduce the total to single digit
        result = self.reduce_to_single_digit(total)
        logger.debug(f"Reduction calculation for '{text}': {result}")
        return result


class ReverseOrdinalCalculator(GematriaCalculator):
    """
    Reverse ordinal gematria calculator.
    Maps z=1, y=2, x=3, ..., a=26
    """
    
    name = "reverse_ordinal"
    description = "Reverse English gematria (z=1, y=2, ..., a=26)"
    
    def calculate(self, text: str) -> int:
        """
        Calculate reverse ordinal value.
        
        Args:
            text: Input text
            
        Returns:
            Sum of reverse ordinal values
        """
        cleaned = self.clean_text(text)
        total = sum(ord('z') - ord(char) + 1 for char in cleaned)
        logger.debug(f"Reverse ordinal calculation for '{text}': {total}")
        return total


class ReverseReductionCalculator(GematriaCalculator):
    """
    Reverse reduction gematria calculator.
    Calculate reverse ordinal, then reduce to single digit.
    """
    
    name = "reverse_reduction"
    description = "Reverse ordinal value reduced to single digit"
    
    def calculate(self, text: str) -> int:
        """
        Calculate reverse reduction value.
        
        Args:
            text: Input text
            
        Returns:
            Single digit after reverse reduction
        """
        cleaned = self.clean_text(text)
        # Calculate reverse ordinal for each letter and reduce individually
        total = sum(
            self.reduce_to_single_digit(ord('z') - ord(char) + 1)
            for char in cleaned
        )
        # Reduce the total to single digit
        result = self.reduce_to_single_digit(total)
        logger.debug(f"Reverse reduction calculation for '{text}': {result}")
        return result


class SumerianCalculator(GematriaCalculator):
    """
    Sumerian gematria calculator.
    Ordinal value multiplied by 6.
    Maps a=6, b=12, c=18, ..., z=156
    """
    
    name = "sumerian"
    description = "Ordinal × 6 (a=6, b=12, c=18, ..., z=156)"
    
    def calculate(self, text: str) -> int:
        """
        Calculate Sumerian value.
        
        Args:
            text: Input text
            
        Returns:
            Sum of Sumerian values (ordinal × 6)
        """
        cleaned = self.clean_text(text)
        total = sum((ord(char) - ord('a') + 1) * 6 for char in cleaned)
        logger.debug(f"Sumerian calculation for '{text}': {total}")
        return total
