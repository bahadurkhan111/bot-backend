"""
Test live prediction with the complete system
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from datetime import date
from apps.predictions.formula import apply_formula
from apps.number_properties.models import NumberProperty
from apps.models_ml.loader import ModelLoader

def test_live_prediction():
    """Test a real prediction with all components."""
    
    print("=" * 70)
    print("LIVE PREDICTION TEST")
    print("=" * 70)
    
    # Example game data
    game_date = date(2026, 1, 14)  # January 14, 2026
    home_team = "Lakers"
    away_team = "Celtics"
    sport = "NBA"
    
    print(f"\nGame: {away_team} @ {home_team}")
    print(f"Date: {game_date.strftime('%B %d, %Y')}")
    print(f"Sport: {sport}")
    print(f"Day of month: {game_date.day}")
    
    # Step 1: Get Pd from database
    print("\n" + "=" * 70)
    print("STEP 1: Get Pd value from database")
    print("=" * 70)
    
    try:
        prop = NumberProperty.objects.get(number=game_date.day)
        pd_value = prop.pd_value
        print(f"✓ Day {game_date.day}: Pd = {pd_value} ({prop.primary_sequence})")
    except NumberProperty.DoesNotExist:
        print(f"✗ No Pd value found for day {game_date.day}")
        return
    
    # Step 2: Get Linear model output (simulated for now)
    print("\n" + "=" * 70)
    print("STEP 2: Get Linear Regression prediction")
    print("=" * 70)
    
    # Try to load real model
    try:
        loader = ModelLoader()
        models = loader.load_all()
        
        if 'linear' in models:
            print("✓ Linear model loaded successfully")
            # For real prediction, we would need actual features:
            # linear_output = models['linear'].predict([features])[0]
            # For now, simulate:
            linear_output = 6.32
            print(f"  (Simulated) Linear output: {linear_output}")
        else:
            print("⚠ Linear model not available, using simulated value")
            linear_output = 6.32
            print(f"  Linear output (simulated): {linear_output}")
    except Exception as e:
        print(f"⚠ Could not load models: {e}")
        linear_output = 6.32
        print(f"  Using simulated Linear output: {linear_output}")
    
    # Step 3: Apply formula
    print("\n" + "=" * 70)
    print("STEP 3: Apply prediction formula")
    print("=" * 70)
    
    result = apply_formula(
        linear_output=linear_output,
        day_of_month=game_date.day,
        sport=sport
    )
    
    print()
    for step in result['formula_steps']:
        print(f"  {step}")
    
    # Final result
    print("\n" + "=" * 70)
    print("FINAL PREDICTION")
    print("=" * 70)
    print(f"\n🏀 {away_team} @ {home_team}")
    print(f"📅 {game_date.strftime('%B %d, %Y')}")
    print(f"\n🎯 Predicted Total: {result['predicted_total']:.2f} points")
    print(f"   (Truest Number: {result['truest_number']} × {result['sport_multiplier']})")
    print("\n" + "=" * 70)
    
    return result


def test_multiple_scenarios():
    """Test multiple game scenarios."""
    
    print("\n\n" + "=" * 70)
    print("TESTING MULTIPLE GAME SCENARIOS")
    print("=" * 70)
    
    scenarios = [
        {"day": 1, "sport": "NBA", "linear": 5.0, "game": "Warriors @ Lakers"},
        {"day": 7, "sport": "NFL", "linear": 6.5, "game": "Patriots @ Chiefs"},
        {"day": 14, "sport": "NBA", "linear": 6.32, "game": "Celtics @ Lakers"},
        {"day": 21, "sport": "MLB", "linear": 7.8, "game": "Yankees @ Red Sox"},
        {"day": 28, "sport": "NHL", "linear": 4.5, "game": "Bruins @ Maple Leafs"},
    ]
    
    print(f"\n{'Day':<5} {'Sport':<8} {'Pd':<4} {'Sequence':<20} {'Linear':<8} {'Result':<8} {'Game':<30}")
    print("-" * 100)
    
    for scenario in scenarios:
        try:
            prop = NumberProperty.objects.get(number=scenario['day'])
            result = apply_formula(
                linear_output=scenario['linear'],
                day_of_month=scenario['day'],
                sport=scenario['sport']
            )
            
            print(f"{scenario['day']:<5} {scenario['sport']:<8} {prop.pd_value:<4} "
                  f"{prop.primary_sequence:<20} {scenario['linear']:<8.2f} "
                  f"{result['predicted_total']:<8.2f} {scenario['game']:<30}")
        except Exception as e:
            print(f"{scenario['day']:<5} ERROR: {e}")
    
    print("=" * 100)


def test_all_days():
    """Show predictions for all days 1-31."""
    
    print("\n\n" + "=" * 70)
    print("PREDICTIONS FOR ALL DAYS (1-31)")
    print("=" * 70)
    print("\nUsing: L=6.0 (constant), Sport=NBA (1.15)")
    print()
    print(f"{'Day':<5} {'Pd':<4} {'Sequence':<20} {'Intermediate':<12} {'T':<3} {'Total':<8}")
    print("-" * 70)
    
    linear = 6.0
    sport = "NBA"
    
    for day in range(1, 32):
        try:
            result = apply_formula(
                linear_output=linear,
                day_of_month=day,
                sport=sport
            )
            prop = NumberProperty.objects.get(number=day)
            
            print(f"{day:<5} {prop.pd_value:<4} {prop.primary_sequence:<20} "
                  f"{result['intermediate_value']:<12.2f} {result['truest_number']:<3} "
                  f"{result['predicted_total']:<8.2f}")
        except Exception as e:
            print(f"{day:<5} ERROR: {e}")
    
    print("=" * 70)


if __name__ == '__main__':
    # Run all tests
    test_live_prediction()
    test_multiple_scenarios()
    test_all_days()
    
    print("\n\n✅ All live tests completed!")
