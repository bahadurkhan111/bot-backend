"""
Interactive test using Django shell

Run this with: python manage.py shell < test_shell.py

Or copy-paste into shell: python manage.py shell
"""

from datetime import date
from apps.predictions.formula import apply_formula, calculate_prediction_breakdown
from apps.number_properties.models import NumberProperty

# Test 1: Simple prediction
print("=" * 70)
print("TEST 1: Simple Prediction")
print("=" * 70)

result = apply_formula(
    linear_output=6.32,
    day_of_month=14,
    sport='NBA'
)

print(f"\n🏀 Prediction for January 14, 2026 (NBA)")
print(f"   Linear output: 6.32")
print(f"   Predicted total: {result['predicted_total']:.2f} points")

# Test 2: Check Pd values for all days
print("\n\n" + "=" * 70)
print("TEST 2: Pd Values for All Days")
print("=" * 70)

for day in [1, 7, 14, 21, 28, 31]:
    prop = NumberProperty.objects.get(number=day)
    print(f"Day {day:2d}: Pd={prop.pd_value:2d} ({prop.primary_sequence})")

# Test 3: Different sports
print("\n\n" + "=" * 70)
print("TEST 3: Same Day, Different Sports")
print("=" * 70)

day = 14
linear = 6.32

for sport in ['NBA', 'NFL', 'MLB', 'NHL', 'UFC']:
    result = apply_formula(linear_output=linear, day_of_month=day, sport=sport)
    print(f"{sport:8} → {result['predicted_total']:6.2f} points (multiplier: {result['sport_multiplier']})")

# Test 4: Get detailed breakdown
print("\n\n" + "=" * 70)
print("TEST 4: Detailed Breakdown")
print("=" * 70)

total, breakdown = calculate_prediction_breakdown(
    linear_output=6.32,
    day_of_month=14,
    sport='NBA'
)

print(f"\nTotal: {total:.2f} points\n")
print("Steps:")
for step in breakdown['formula_steps']:
    print(f"  {step}")

print("\n✅ All shell tests completed!")
