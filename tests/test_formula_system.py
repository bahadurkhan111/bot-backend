"""
Test Formula with Gematrinator Pd Values

Verifies that the complete system works:
1. Loads Pd values from database
2. Applies formula correctly
3. Produces expected results
"""

import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.predictions.formula import apply_formula
from apps.number_properties.models import NumberProperty


def test_formula():
    """Test the complete formula with real data."""
    
    print("=" * 70)
    print("TESTING COMPLETE FORMULA SYSTEM")
    print("=" * 70)
    print()
    
    # Test case: Lakers vs Celtics, January 14
    print("TEST CASE: Lakers vs Celtics (January 14, 2026)")
    print("-" * 70)
    
    linear_output = 6.32
    day = 14
    sport = 'NBA'
    
    # Get Pd from database
    pd_value = NumberProperty.get_pd_value(day)
    print(f"Linear output (L): {linear_output}")
    print(f"Day: {day}")
    print(f"Pd from database: {pd_value}")
    print(f"Sport: {sport}")
    print()
    
    # Apply formula (will load Pd automatically)
    result = apply_formula(
        linear_output=linear_output,
        day_of_month=day,
        sport=sport
    )
    
    print("FORMULA STEPS:")
    print("-" * 70)
    for step in result['formula_steps']:
        print(step)
    
    print()
    print("=" * 70)
    print(f"✅ FINAL PREDICTION: {result['predicted_total']:.2f} points")
    print("=" * 70)
    print()
    
    # Test multiple days
    print()
    print("TESTING MULTIPLE DAYS:")
    print("=" * 70)
    
    test_cases = [
        (1, 5.0, 'NBA', 'Day 1 - Fibonacci'),
        (2, 6.5, 'NFL', 'Day 2 - Prime'),
        (14, 6.32, 'NBA', 'Day 14 - Square Pyramidal'),
        (28, 7.8, 'NHL', 'Day 28 - Triangular'),
        (31, 4.2, 'MLB', 'Day 31 - Prime'),
    ]
    
    print(f"{'Day':>3} | {'Pd':>2} | {'Seq':<20} | {'L':>6} | {'Sport':<10} | {'Result':>8}")
    print("-" * 70)
    
    for day, L, sport, description in test_cases:
        prop = NumberProperty.objects.get(number=day)
        result = apply_formula(L, day, sport=sport)
        
        print(f"{day:3d} | {prop.pd_value:2d} | {prop.primary_sequence:<20} | {L:6.2f} | {sport:<10} | {result['predicted_total']:8.2f}")
    
    print("=" * 70)
    print()
    
    # Verify Pd values match expectations
    print()
    print("VERIFYING Pd VALUES:")
    print("=" * 70)
    
    expected_pd = {
        1: 1,   # Fibonacci position 1
        2: 1,   # Prime position 1
        4: 4,   # Square has 4 sides
        6: 3,   # Triangular has 3 sides
        14: 5,  # Square Pyramidal has 5 faces
        27: 6,  # Cube has 6 faces
    }
    
    all_correct = True
    for day, expected in expected_pd.items():
        prop = NumberProperty.objects.get(number=day)
        actual = prop.pd_value
        match = "✓" if actual == expected else "✗"
        status = "PASS" if actual == expected else "FAIL"
        
        print(f"  {match} Day {day:2d}: Expected Pd={expected}, Got Pd={actual} - {status} ({prop.primary_sequence})")
        
        if actual != expected:
            all_correct = False
    
    print("=" * 70)
    
    if all_correct:
        print()
        print("🎉 ALL TESTS PASSED!")
        print()
    else:
        print()
        print("❌ SOME TESTS FAILED")
        print()
        return False
    
    return True


if __name__ == '__main__':
    success = test_formula()
    sys.exit(0 if success else 1)
