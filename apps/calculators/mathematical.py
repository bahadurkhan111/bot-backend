"""
Mathematical gematria calculators: Primes, Trigonal, Squares, Fibonacci.
"""
from .base import GematriaCalculator
import logging

logger = logging.getLogger(__name__)


class PrimesCalculator(GematriaCalculator):
    """
    Primes gematria calculator.
    Uses prime numbers sequence: a=2, b=3, c=5, d=7, e=11, etc.
    """
    
    name = "primes"
    description = "Prime numbers (a=2, b=3, c=5, d=7, e=11, ...)"
    
    # First 26 prime numbers
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    
    def calculate(self, text: str) -> int:
        """Calculate Primes value."""
        cleaned = self.clean_text(text)
        total = sum(self.PRIMES[ord(char) - ord('a')] for char in cleaned)
        logger.debug(f"Primes calculation for '{text}': {total}")
        return total


class TrigonalCalculator(GematriaCalculator):
    """
    Trigonal (Triangular) gematria calculator.
    Uses triangular numbers: a=1, b=3, c=6, d=10, e=15, etc.
    Formula: T(n) = n(n+1)/2
    """
    
    name = "trigonal"
    description = "Triangular numbers (a=1, b=3, c=6, d=10, ...)"
    
    def calculate(self, text: str) -> int:
        """Calculate Trigonal value."""
        cleaned = self.clean_text(text)
        total = 0
        for char in cleaned:
            n = ord(char) - ord('a') + 1
            triangular = n * (n + 1) // 2
            total += triangular
        logger.debug(f"Trigonal calculation for '{text}': {total}")
        return total


class SquaresCalculator(GematriaCalculator):
    """
    Squares gematria calculator.
    Uses square numbers: a=1, b=4, c=9, d=16, etc.
    Formula: n²
    """
    
    name = "squares"
    description = "Square numbers (a=1, b=4, c=9, d=16, ...)"
    
    def calculate(self, text: str) -> int:
        """Calculate Squares value."""
        cleaned = self.clean_text(text)
        total = 0
        for char in cleaned:
            n = ord(char) - ord('a') + 1
            total += n * n
        logger.debug(f"Squares calculation for '{text}': {total}")
        return total


class FibonacciCalculator(GematriaCalculator):
    """
    Fibonacci gematria calculator.
    Uses Fibonacci sequence: a=1, b=1, c=2, d=3, e=5, f=8, etc.
    """
    
    name = "fibonacci"
    description = "Fibonacci sequence (a=1, b=1, c=2, d=3, e=5, f=8, ...)"
    
    # First 26 Fibonacci numbers
    FIB = [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610,
           987, 1597, 2584, 4181, 6765, 10946, 17711, 28657, 46368, 75025, 121393]
    
    def calculate(self, text: str) -> int:
        """Calculate Fibonacci value."""
        cleaned = self.clean_text(text)
        total = sum(self.FIB[ord(char) - ord('a')] for char in cleaned)
        logger.debug(f"Fibonacci calculation for '{text}': {total}")
        return total


class ReversePrimesCalculator(GematriaCalculator):
    """Reverse Primes calculator (z=2, y=3, etc.)"""
    
    name = "reverse_primes"
    description = "Reverse prime numbers"
    
    PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 
              53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
    
    def calculate(self, text: str) -> int:
        """Calculate Reverse Primes value."""
        cleaned = self.clean_text(text)
        total = sum(self.PRIMES[ord('z') - ord(char)] for char in cleaned)
        logger.debug(f"Reverse Primes calculation for '{text}': {total}")
        return total


class ReverseTrigonalCalculator(GematriaCalculator):
    """Reverse Trigonal calculator"""
    
    name = "reverse_trigonal"
    description = "Reverse triangular numbers"
    
    def calculate(self, text: str) -> int:
        """Calculate Reverse Trigonal value."""
        cleaned = self.clean_text(text)
        total = 0
        for char in cleaned:
            n = ord('z') - ord(char) + 1
            triangular = n * (n + 1) // 2
            total += triangular
        logger.debug(f"Reverse Trigonal calculation for '{text}': {total}")
        return total
