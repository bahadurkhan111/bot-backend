"""
Date Calculator - 13 Numerological Calculations

Implements the client's date-based numerology system for sports predictions.
Based on the original JavaScript DateCalc-207.js formula.
"""

from datetime import datetime
from typing import Dict, List
import calendar


class DateCalculator:
    """Calculate 13 date-based numerologies for any given date."""
    
    @staticmethod
    def calculate_all(date: datetime) -> Dict[str, int]:
        """
        Calculate all 13 numerologies for a given date.
        
        Args:
            date: datetime object to calculate numerologies for
            
        Returns:
            Dictionary with 13 numerology values
            
        Example:
            For date 01/14/2026:
            {
                'num1': 61,   # month + day + (20) + (26)
                'num2': 25,   # month + day + 2+0+2+6
                'num3': 16,   # All digits: 0+1+1+4+2+0+2+6
                'num4': 41,   # month + day + (26)
                'num5': 14,   # Digits without century: 0+1+1+4+2+6
                'num6': 14,   # Day of year
                'num7': 351,  # Days left in year
                'num8': 15,   # month + day
                'num9': 52,   # 0+1+1+4+20+26
                'num10': 23,  # month + day + 2+6
                'num11': 32,  # 0+1+1+4+26
                'num12': 0,   # Product: 1×1×4×2×0×2×6
                'num13': 48   # Product: 1×1×4×2×6 (last 2 digits)
            }
        """
        month = date.month
        day = date.day
        year = date.year
        
        # Extract year components
        century = year // 100  # 20 for 2026
        decade = year % 100    # 26 for 2026
        
        # Get digits
        month_digits = DateCalculator._get_digits(month)
        day_digits = DateCalculator._get_digits(day)
        year_digits = DateCalculator._get_digits(year)
        decade_digits = DateCalculator._get_digits(decade)
        
        # Calculate day of year and days remaining
        day_of_year = date.timetuple().tm_yday
        is_leap = calendar.isleap(year)
        days_in_year = 366 if is_leap else 365
        days_remaining = days_in_year - day_of_year
        
        # Numerology 1: month + day + (20) + (26)
        num1 = month + day + century + decade
        
        # Numerology 2: month + day + 2+0+2+6
        num2 = month + day + sum(year_digits)
        
        # Numerology 3: 0+1+1+4+2+0+2+6 (all digits)
        num3 = sum(month_digits) + sum(day_digits) + sum(year_digits)
        
        # Numerology 4: month + day + (26)
        num4 = month + day + decade
        
        # Numerology 5: 0+1+1+4+2+6 (digits without century)
        num5 = sum(month_digits) + sum(day_digits) + sum(decade_digits)
        
        # Numerology 6: Day of year
        num6 = day_of_year
        
        # Numerology 7: Days left in year
        num7 = days_remaining
        
        # Numerology 8: month + day
        num8 = month + day
        
        # Numerology 9: 0+1+1+4+20+26
        num9 = sum(month_digits) + sum(day_digits) + century + decade
        
        # Numerology 10: month + day + 2+6
        num10 = month + day + sum(decade_digits)
        
        # Numerology 11: 0+1+1+4+26
        num11 = sum(month_digits) + sum(day_digits) + decade
        
        # Numerology 12: 1×1×4×2×0×2×6 (full year product)
        # For products, use raw digits without leading zeros
        month_raw = DateCalculator._get_digits_raw(month)
        day_raw = DateCalculator._get_digits_raw(day)
        year_raw = DateCalculator._get_digits_raw(year)
        decade_raw = DateCalculator._get_digits_raw(decade)
        
        num12 = DateCalculator._product_of_digits(
            month_raw + day_raw + year_raw
        )
        
        # Numerology 13: 1×1×4×2×6 (last 2 digits product)
        num13 = DateCalculator._product_of_digits(
            month_raw + day_raw + decade_raw
        )
        
        return {
            'num1': num1,
            'num2': num2,
            'num3': num3,
            'num4': num4,
            'num5': num5,
            'num6': num6,
            'num7': num7,
            'num8': num8,
            'num9': num9,
            'num10': num10,
            'num11': num11,
            'num12': num12,
            'num13': num13,
        }
    
    @staticmethod
    def _get_digits(number: int) -> List[int]:
        """
        Extract individual digits from a number.
        
        Examples:
            14 -> [1, 4]
            2026 -> [2, 0, 2, 6]
            5 -> [0, 5] (padded for month/day)
        """
        # Pad single digits with 0 for month/day (01, 02, etc.)
        if number < 10:
            return [0, number]
        return [int(d) for d in str(number)]
    
    @staticmethod
    def _get_digits_raw(number: int) -> List[int]:
        """
        Extract individual digits without padding.
        Used for product calculations where leading zeros should not be included.
        
        Examples:
            1 -> [1]
            14 -> [1, 4]
            26 -> [2, 6]
            2026 -> [2, 0, 2, 6]
        """
        return [int(d) for d in str(number)]
    
    @staticmethod
    def _product_of_digits(digits: List[int]) -> int:
        """
        Calculate the product of a list of digits.
        
        Examples:
            [1, 2, 3] -> 6
            [1, 0, 5] -> 0
        """
        product = 1
        for digit in digits:
            product *= digit
        return product
    
    @staticmethod
    def calculate_single(date: datetime, numerology_number: int) -> int:
        """
        Calculate a specific numerology (1-13) for a date.
        
        Args:
            date: datetime object
            numerology_number: Which numerology to calculate (1-13)
            
        Returns:
            The calculated numerology value
        """
        all_numerologies = DateCalculator.calculate_all(date)
        key = f'num{numerology_number}'
        
        if key not in all_numerologies:
            raise ValueError(f"Invalid numerology number: {numerology_number}. Must be 1-13.")
        
        return all_numerologies[key]
    
    @staticmethod
    def get_numerology_descriptions() -> Dict[int, str]:
        """
        Get human-readable descriptions for each numerology.
        
        Returns:
            Dictionary mapping numerology number to description
        """
        return {
            1: "Month + Day + Century + Decade (e.g., 1+14+20+26)",
            2: "Month + Day + Year Digits Sum (e.g., 1+14+2+0+2+6)",
            3: "All Digits Sum (e.g., 0+1+1+4+2+0+2+6)",
            4: "Month + Day + Decade (e.g., 1+14+26)",
            5: "Digits Without Century (e.g., 0+1+1+4+2+6)",
            6: "Day of Year (1-365/366)",
            7: "Days Remaining in Year",
            8: "Month + Day (e.g., 1+14)",
            9: "Month Digits + Day Digits + Century + Decade (e.g., 0+1+1+4+20+26)",
            10: "Month + Day + Decade Digits Sum (e.g., 1+14+2+6)",
            11: "Month Digits + Day Digits + Decade (e.g., 0+1+1+4+26)",
            12: "Product of All Digits with Full Year (e.g., 1×1×4×2×0×2×6)",
            13: "Product of Digits with Last 2 Year Digits (e.g., 1×1×4×2×6)",
        }
