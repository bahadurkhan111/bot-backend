"""
Multiplier-based gematria calculators.
"""
from .base import GematriaCalculator
import logging

logger = logging.getLogger(__name__)


class ReverseSumerianCalculator(GematriaCalculator):
    """
    Reverse Sumerian gematria calculator.
    Reverse ordinal value multiplied by 6.
    Maps z=6, y=12, x=18, ..., a=156
    """
    
    name = "reverse_sumerian"
    description = "Reverse ordinal × 6 (z=6, y=12, ..., a=156)"
    
    def calculate(self, text: str) -> int:
        """Calculate Reverse Sumerian value."""
        cleaned = self.clean_text(text)
        total = sum((ord('z') - ord(char) + 1) * 6 for char in cleaned)
        logger.debug(f"Reverse Sumerian calculation for '{text}': {total}")
        return total


class SatanicCalculator(GematriaCalculator):
    """
    Satanic gematria calculator.
    Ordinal value multiplied by 36.
    Maps a=36, b=72, c=108, ..., z=936
    """
    
    name = "satanic"
    description = "Ordinal × 36 (a=36, b=72, c=108, ..., z=936)"
    
    def calculate(self, text: str) -> int:
        """Calculate Satanic value."""
        cleaned = self.clean_text(text)
        total = sum((ord(char) - ord('a') + 1) * 36 for char in cleaned)
        logger.debug(f"Satanic calculation for '{text}': {total}")
        return total


class ReverseSatanicCalculator(GematriaCalculator):
    """
    Reverse Satanic gematria calculator.
    Reverse ordinal value multiplied by 36.
    """
    
    name = "reverse_satanic"
    description = "Reverse ordinal × 36"
    
    def calculate(self, text: str) -> int:
        """Calculate Reverse Satanic value."""
        cleaned = self.clean_text(text)
        total = sum((ord('z') - ord(char) + 1) * 36 for char in cleaned)
        logger.debug(f"Reverse Satanic calculation for '{text}': {total}")
        return total
