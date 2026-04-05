"""
Special gematria calculators: Chaldean, Latin, Jewish, etc.
"""
from .base import GematriaCalculator
import logging

logger = logging.getLogger(__name__)


class ChaldeanCalculator(GematriaCalculator):
    """
    Chaldean numerology calculator.
    Ancient Babylonian system: a=1, b=2, c=3, d=4, e=5, u=6, o=7, f=8
    Note: No 9 in Chaldean numerology
    """
    
    name = "chaldean"
    description = "Chaldean numerology (ancient system, no 9)"
    
    CHALDEAN_MAP = {
        'a': 1, 'i': 1, 'j': 1, 'q': 1, 'y': 1,
        'b': 2, 'k': 2, 'r': 2,
        'c': 3, 'g': 3, 'l': 3, 's': 3,
        'd': 4, 'm': 4, 't': 4,
        'e': 5, 'h': 5, 'n': 5, 'x': 5,
        'u': 6, 'v': 6, 'w': 6,
        'o': 7, 'z': 7,
        'f': 8, 'p': 8
    }
    
    def calculate(self, text: str) -> int:
        """Calculate Chaldean value."""
        cleaned = self.clean_text(text)
        total = sum(self.CHALDEAN_MAP.get(char, 0) for char in cleaned)
        logger.debug(f"Chaldean calculation for '{text}': {total}")
        return total


class LatinCalculator(GematriaCalculator):
    """Latin Ordinal calculator (same as Ordinal)"""
    
    name = "latin"
    description = "Latin ordinal (a=1, b=2, ..., z=26)"
    
    def calculate(self, text: str) -> int:
        """Calculate Latin value."""
        cleaned = self.clean_text(text)
        total = sum(ord(char) - ord('a') + 1 for char in cleaned)
        logger.debug(f"Latin calculation for '{text}': {total}")
        return total


class LatinReductionCalculator(GematriaCalculator):
    """Latin Reduction calculator"""
    
    name = "latin_reduction"
    description = "Latin reduction to single digit"
    
    def calculate(self, text: str) -> int:
        """Calculate Latin Reduction value."""
        cleaned = self.clean_text(text)
        total = sum(
            self.reduce_to_single_digit(ord(char) - ord('a') + 1)
            for char in cleaned
        )
        result = self.reduce_to_single_digit(total)
        logger.debug(f"Latin Reduction calculation for '{text}': {result}")
        return result


class SeptenaryCalculator(GematriaCalculator):
    """
    Septenary calculator (7-based system).
    Cycles through 1-7: a=1, b=2, c=3, d=4, e=5, f=6, g=7, h=1, i=2, etc.
    """
    
    name = "septenary"
    description = "7-based system (cycles 1-7)"
    
    def calculate(self, text: str) -> int:
        """Calculate Septenary value."""
        cleaned = self.clean_text(text)
        total = 0
        for char in cleaned:
            position = ord(char) - ord('a') + 1
            value = ((position - 1) % 7) + 1
            total += value
        logger.debug(f"Septenary calculation for '{text}': {total}")
        return total


class KeypadCalculator(GematriaCalculator):
    """
    Phone Keypad calculator.
    Based on phone keypad: abc=2, def=3, ghi=4, etc.
    """
    
    name = "keypad"
    description = "Phone keypad (abc=2, def=3, ghi=4, ...)"
    
    KEYPAD_MAP = {
        'a': 2, 'b': 2, 'c': 2,
        'd': 3, 'e': 3, 'f': 3,
        'g': 4, 'h': 4, 'i': 4,
        'j': 5, 'k': 5, 'l': 5,
        'm': 6, 'n': 6, 'o': 6,
        'p': 7, 'q': 7, 'r': 7, 's': 7,
        't': 8, 'u': 8, 'v': 8,
        'w': 9, 'x': 9, 'y': 9, 'z': 9
    }
    
    def calculate(self, text: str) -> int:
        """Calculate Keypad value."""
        cleaned = self.clean_text(text)
        total = sum(self.KEYPAD_MAP.get(char, 0) for char in cleaned)
        logger.debug(f"Keypad calculation for '{text}': {total}")
        return total


class FrancisBaconCalculator(GematriaCalculator):
    """
    Francis Bacon calculator.
    a=1, b=2, ..., j/u=10, k/v=11, ..., z=24
    """
    
    name = "francis_bacon"
    description = "Francis Bacon cipher (j/u share, k/v share)"
    
    BACON_MAP = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 10, 'k': 11, 'l': 12, 'm': 13, 'n': 14, 'o': 15, 'p': 16, 'q': 17,
        'r': 18, 's': 19, 't': 20, 'u': 10, 'v': 11, 'w': 22, 'x': 23, 'y': 24, 'z': 25
    }
    
    def calculate(self, text: str) -> int:
        """Calculate Francis Bacon value."""
        cleaned = self.clean_text(text)
        total = sum(self.BACON_MAP.get(char, 0) for char in cleaned)
        logger.debug(f"Francis Bacon calculation for '{text}': {total}")
        return total


class EnglishOrdinalCalculator(GematriaCalculator):
    """English Ordinal (same as Ordinal)"""
    
    name = "english_ordinal"
    description = "English ordinal (a=1, b=2, ..., z=26)"
    
    def calculate(self, text: str) -> int:
        """Calculate English Ordinal value."""
        cleaned = self.clean_text(text)
        total = sum(ord(char) - ord('a') + 1 for char in cleaned)
        logger.debug(f"English Ordinal calculation for '{text}': {total}")
        return total


class EnglishReductionCalculator(GematriaCalculator):
    """English Reduction calculator"""
    
    name = "english_reduction"
    description = "English reduction to single digit"
    
    def calculate(self, text: str) -> int:
        """Calculate English Reduction value."""
        cleaned = self.clean_text(text)
        total = sum(
            self.reduce_to_single_digit(ord(char) - ord('a') + 1)
            for char in cleaned
        )
        result = self.reduce_to_single_digit(total)
        logger.debug(f"English Reduction calculation for '{text}': {result}")
        return result


class SingleReductionCalculator(GematriaCalculator):
    """
    Single Reduction with exceptions.
    S=10, K=11, V=22 (not reduced)
    """
    
    name = "single_reduction"
    description = "Single reduction with S=10, K=11, V=22 exceptions"
    
    def calculate(self, text: str) -> int:
        """Calculate Single Reduction value."""
        cleaned = self.clean_text(text)
        total = 0
        for char in cleaned:
            if char == 's':
                total += 10
            elif char == 'k':
                total += 11
            elif char == 'v':
                total += 22
            else:
                value = ord(char) - ord('a') + 1
                total += self.reduce_to_single_digit(value)
        logger.debug(f"Single Reduction calculation for '{text}': {total}")
        return total


class JewishCalculator(GematriaCalculator):
    """Jewish Gematria (Hebrew-based)"""
    
    name = "jewish"
    description = "Jewish gematria (Hebrew letter values)"
    
    JEWISH_MAP = {
        'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8, 'i': 9,
        'j': 10, 'k': 20, 'l': 30, 'm': 40, 'n': 50, 'o': 60, 'p': 70, 'q': 80,
        'r': 90, 's': 100, 't': 200, 'u': 300, 'v': 400, 'w': 500, 'x': 600,
        'y': 700, 'z': 800
    }
    
    def calculate(self, text: str) -> int:
        """Calculate Jewish value."""
        cleaned = self.clean_text(text)
        total = sum(self.JEWISH_MAP.get(char, 0) for char in cleaned)
        logger.debug(f"Jewish calculation for '{text}': {total}")
        return total


class ALWKabbalahCalculator(GematriaCalculator):
    """ALW Kabbalah calculator"""
    
    name = "alw_kabbalah"
    description = "ALW Kabbalah cipher"
    
    ALW_MAP = {
        'a': 1, 'l': 2, 'w': 3, 'h': 4, 's': 5, 'd': 6, 'o': 7, 'z': 8, 'k': 9,
        'v': 10, 'g': 11, 'r': 12, 'c': 13, 'n': 14, 'y': 15, 'j': 16, 'u': 17,
        'f': 18, 'q': 19, 'b': 20, 'm': 21, 'x': 22, 'i': 23, 't': 24, 'e': 25, 'p': 26
    }
    
    def calculate(self, text: str) -> int:
        """Calculate ALW Kabbalah value."""
        cleaned = self.clean_text(text)
        total = sum(self.ALW_MAP.get(char, 0) for char in cleaned)
        logger.debug(f"ALW Kabbalah calculation for '{text}': {total}")
        return total


class KFWKabbalahCalculator(GematriaCalculator):
    """KFW Kabbalah calculator"""
    
    name = "kfw_kabbalah"
    description = "KFW Kabbalah cipher"
    
    KFW_MAP = {
        'k': 1, 'f': 2, 'w': 3, 'r': 4, 'm': 5, 'x': 6, 'i': 7, 't': 8, 'e': 9,
        'p': 10, 'a': 11, 'l': 12, 'b': 13, 'g': 14, 'c': 15, 'h': 16, 'd': 17,
        'n': 18, 'o': 19, 'y': 20, 'j': 21, 'u': 22, 'q': 23, 'v': 24, 's': 25, 'z': 26
    }
    
    def calculate(self, text: str) -> int:
        """Calculate KFW Kabbalah value."""
        cleaned = self.clean_text(text)
        total = sum(self.KFW_MAP.get(char, 0) for char in cleaned)
        logger.debug(f"KFW Kabbalah calculation for '{text}': {total}")
        return total
