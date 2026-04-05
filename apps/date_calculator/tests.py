"""
Tests for Date Calculator App
"""

from django.test import TestCase
from datetime import datetime, date
from .calculator import DateCalculator
from .models import DateNumerology


class DateCalculatorTestCase(TestCase):
    """Test the DateCalculator class."""
    
    def test_calculate_all_example_date(self):
        """Test calculation for example date 01/14/2026 from specification."""
        test_date = datetime(2026, 1, 14)
        calculator = DateCalculator()
        result = calculator.calculate_all(test_date)
        
        # Expected values from specification
        self.assertEqual(result['num1'], 61)   # 1+14+20+26 = 61
        self.assertEqual(result['num2'], 25)   # 1+14+2+0+2+6 = 25
        self.assertEqual(result['num3'], 16)   # 0+1+1+4+2+0+2+6 = 16
        self.assertEqual(result['num4'], 41)   # 1+14+26 = 41
        self.assertEqual(result['num5'], 14)   # 0+1+1+4+2+6 = 14
        self.assertEqual(result['num6'], 14)   # Day of year = 14
        self.assertEqual(result['num7'], 351)  # Days left = 351
        self.assertEqual(result['num8'], 15)   # 1+14 = 15
        self.assertEqual(result['num9'], 52)   # 0+1+1+4+20+26 = 52
        self.assertEqual(result['num10'], 23)  # 1+14+2+6 = 23
        self.assertEqual(result['num11'], 32)  # 0+1+1+4+26 = 32
        self.assertEqual(result['num12'], 0)   # 1×1×4×2×0×2×6 = 0
        self.assertEqual(result['num13'], 48)  # 1×1×4×2×6 = 48
    
    def test_calculate_single_numerology(self):
        """Test calculating a single numerology value."""
        test_date = datetime(2026, 1, 14)
        calculator = DateCalculator()
        
        # Test specific numerology
        num6 = calculator.calculate_single(test_date, 6)
        self.assertEqual(num6, 14)  # Day of year
        
        num8 = calculator.calculate_single(test_date, 8)
        self.assertEqual(num8, 15)  # month + day
    
    def test_invalid_numerology_number(self):
        """Test error handling for invalid numerology number."""
        test_date = datetime(2026, 1, 14)
        calculator = DateCalculator()
        
        with self.assertRaises(ValueError):
            calculator.calculate_single(test_date, 0)
        
        with self.assertRaises(ValueError):
            calculator.calculate_single(test_date, 14)
    
    def test_leap_year_calculation(self):
        """Test calculations for leap year date."""
        # 2024 is a leap year
        test_date = datetime(2024, 2, 29)
        calculator = DateCalculator()
        result = calculator.calculate_all(test_date)
        
        # Verify day of year for Feb 29
        self.assertEqual(result['num6'], 60)  # 31 (Jan) + 29 (Feb)
        
        # Verify days remaining (366 - 60)
        self.assertEqual(result['num7'], 306)
    
    def test_get_digits(self):
        """Test digit extraction."""
        calculator = DateCalculator()
        
        # Single digit (padded)
        self.assertEqual(calculator._get_digits(5), [0, 5])
        
        # Two digits
        self.assertEqual(calculator._get_digits(14), [1, 4])
        
        # Four digits
        self.assertEqual(calculator._get_digits(2026), [2, 0, 2, 6])
    
    def test_product_of_digits(self):
        """Test product calculation."""
        calculator = DateCalculator()
        
        # Normal product
        self.assertEqual(calculator._product_of_digits([1, 2, 3]), 6)
        
        # Product with zero
        self.assertEqual(calculator._product_of_digits([1, 0, 5]), 0)
        
        # Single digit
        self.assertEqual(calculator._product_of_digits([7]), 7)
    
    def test_descriptions(self):
        """Test numerology descriptions."""
        descriptions = DateCalculator.get_numerology_descriptions()
        
        self.assertEqual(len(descriptions), 13)
        self.assertIn(1, descriptions)
        self.assertIn(13, descriptions)
        self.assertIsInstance(descriptions[1], str)


class DateNumerologyModelTestCase(TestCase):
    """Test the DateNumerology model."""
    
    def test_get_or_calculate_creates_new(self):
        """Test that get_or_calculate creates new entry."""
        test_date = date(2026, 1, 14)
        
        # Should not exist yet
        self.assertEqual(DateNumerology.objects.filter(date=test_date).count(), 0)
        
        # Get or calculate
        numerology = DateNumerology.get_or_calculate(test_date)
        
        # Should exist now
        self.assertEqual(DateNumerology.objects.filter(date=test_date).count(), 1)
        self.assertEqual(numerology.date, test_date)
        self.assertEqual(numerology.num1, 61)
    
    def test_get_or_calculate_retrieves_existing(self):
        """Test that get_or_calculate retrieves cached entry."""
        test_date = date(2026, 1, 14)
        
        # Create first time
        first = DateNumerology.get_or_calculate(test_date)
        first_id = first.id
        
        # Get second time (should be cached)
        second = DateNumerology.get_or_calculate(test_date)
        second_id = second.id
        
        # Should be same instance
        self.assertEqual(first_id, second_id)
        
        # Should still only be one in database
        self.assertEqual(DateNumerology.objects.filter(date=test_date).count(), 1)
    
    def test_to_dict(self):
        """Test to_dict method."""
        test_date = date(2026, 1, 14)
        numerology = DateNumerology.get_or_calculate(test_date)
        
        result = numerology.to_dict()
        
        self.assertIn('date', result)
        self.assertIn('numerologies', result)
        self.assertIn('numerologies_list', result)
        
        self.assertEqual(result['date'], '2026-01-14')
        self.assertEqual(len(result['numerologies_list']), 13)
        self.assertEqual(result['numerologies']['num1'], 61)
    
    def test_str_representation(self):
        """Test string representation."""
        test_date = date(2026, 1, 14)
        numerology = DateNumerology.get_or_calculate(test_date)
        
        self.assertEqual(str(numerology), "Numerologies for 2026-01-14")
