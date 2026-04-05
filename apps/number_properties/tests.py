"""
Tests for Number Properties App
"""

from django.test import TestCase
from .models import NumberProperty


class NumberPropertyModelTestCase(TestCase):
    """Test the NumberProperty model."""
    
    def test_calculate_condensed_number(self):
        """Test numerological reduction calculation."""
        # Single digit
        self.assertEqual(NumberProperty.calculate_condensed_number(5), 5)
        
        # Two digits
        self.assertEqual(NumberProperty.calculate_condensed_number(14), 5)  # 1+4=5
        self.assertEqual(NumberProperty.calculate_condensed_number(19), 1)  # 1+9=10, 1+0=1
        
        # More examples
        self.assertEqual(NumberProperty.calculate_condensed_number(28), 1)  # 2+8=10, 1+0=1
        self.assertEqual(NumberProperty.calculate_condensed_number(31), 4)  # 3+1=4
    
    def test_get_condensed_number_invalid_day(self):
        """Test error handling for invalid days."""
        with self.assertRaises(ValueError):
            NumberProperty.get_condensed_number(0)
        
        with self.assertRaises(ValueError):
            NumberProperty.get_condensed_number(32)
        
        with self.assertRaises(ValueError):
            NumberProperty.get_condensed_number(-5)
    
    def test_create_number_property(self):
        """Test creating a number property."""
        prop = NumberProperty.objects.create(
            number=14,
            condensed_number=5,
            is_prime=False,
            is_composite=True,
            divisors_count=4,
            divisors_list=[1, 2, 7, 14],
            conversion_binary='1110'
        )
        
        self.assertEqual(prop.number, 14)
        self.assertEqual(prop.condensed_number, 5)
        self.assertFalse(prop.is_prime)
        self.assertTrue(prop.is_composite)
        self.assertEqual(str(prop), "Number 14 (condensed: 5)")
    
    def test_to_dict(self):
        """Test to_dict method."""
        prop = NumberProperty.objects.create(
            number=7,
            condensed_number=7,
            is_prime=True,
            prime_position=4,
            divisors_count=2,
            divisors_list=[1, 7]
        )
        
        result = prop.to_dict()
        
        self.assertEqual(result['number'], 7)
        self.assertEqual(result['condensed_number'], 7)
        self.assertTrue(result['sequences']['is_prime'])
        self.assertEqual(result['positions']['prime'], 4)
        self.assertEqual(result['divisors']['count'], 2)
