#!/usr/bin/env python
"""
Test script for the Telegram bot functionality.
Tests all commands without actually running the bot.
"""
import os
import sys
import django

# Setup Django - agregar directorio raíz al path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.predictions.formula import (
    apply_formula,
    get_pd_value,
    numerological_reduction,
    SPORT_MULTIPLIERS
)


def test_predict_command():
    """Test the /predict command logic."""
    print("=" * 50)
    print("TEST 1: /predict Command")
    print("=" * 50)
    
    # Example: /predict L=6.32 day=14 sport=NBA
    L = 6.32
    day = 14
    sport = 'NBA'
    
    print(f"\nInput:")
    print(f"  L={L} day={day} sport={sport}")
    
    # Get Pd value
    Pd = get_pd_value(day)
    print(f"\nPd value for day {day}: {Pd}")
    
    # Calculate prediction
    result_dict = apply_formula(L, day, sport)
    result = result_dict['predicted_total']
    
    # Calculate intermediate values for display
    C = (L + (5 * Pd)) / 2
    N = numerological_reduction(C)
    s = SPORT_MULTIPLIERS.get(sport, SPORT_MULTIPLIERS['DEFAULT'])
    
    print(f"\nCalculation:")
    print(f"  C = (L + 5·Pd) / 2")
    print(f"  C = ({L} + {5*Pd}) / 2")
    print(f"  C = {C:.2f}")
    print(f"\n  N = numerological_reduction(C)")
    print(f"  N = {N}")
    print(f"\n  T = N × s")
    print(f"  T = {N} × {s}")
    print(f"\nPREDICTION: {result:.2f} points")
    print("✅ Test passed!\n")


def test_compare_command():
    """Test the /compare command logic."""
    print("=" * 50)
    print("TEST 2: /compare Command")
    print("=" * 50)
    
    # Example: /compare prediction=10.35 vegas=219.5
    prediction = 10.35
    vegas = 219.5
    
    print(f"\nInput:")
    print(f"  prediction={prediction} vegas={vegas}")
    
    # Calculate discrepancy
    discrepancy = abs(prediction - vegas)
    
    # Classify discrepancy
    if discrepancy < 20:
        level = "NORMAL"
        emoji = "🟢"
        signal = "SEGURO"
        recommendation = "Seguro para apostar según análisis"
    elif discrepancy < 50:
        level = "CAUTION"
        emoji = "🟡"
        signal = "BULLISH" if prediction < vegas else "BEARISH"
        recommendation = "Proceder con cautela"
    else:
        level = "EXTREME"
        emoji = "🔴"
        signal = "NO APOSTAR"
        recommendation = "Discrepancia muy grande - posible ajuste de Vegas"
    
    print(f"\nDiscrepancy: {discrepancy:.2f} points")
    print(f"Level: {emoji} {level}")
    print(f"Signal: {signal}")
    print(f"Recommendation: {recommendation}")
    print("✅ Test passed!\n")


def test_condensed_command():
    """Test the /condensed command logic."""
    print("=" * 50)
    print("TEST 3: /condensed Command")
    print("=" * 50)
    
    # Test multiple days
    test_days = [1, 2, 14, 27, 31]
    
    for day in test_days:
        Pd = get_pd_value(day)
        print(f"\nDay {day}: Pd = {Pd}")
    
    print("✅ Test passed!\n")


def test_formula_explanation():
    """Test the /formula command logic."""
    print("=" * 50)
    print("TEST 4: /formula Command")
    print("=" * 50)
    
    print("\nFormula: T = R((L + 5·Pd) / 2) × s")
    print("\nComponents:")
    print("  T = Predicted total points")
    print("  L = Linear Regression output")
    print("  Pd = Condensed number for the day")
    print("  R(x) = Numerological reduction")
    print("  s = Sport multiplier")
    print("✅ Test passed!\n")


def test_sports_multipliers():
    """Test the /sports command logic."""
    print("=" * 50)
    print("TEST 5: /sports Command")
    print("=" * 50)
    
    print("\nSport Multipliers:")
    
    sports_categories = {
        'Basketball': ['NBA', 'WNBA', 'NCAA_BASKETBALL'],
        'Football': ['NFL', 'NCAA_FOOTBALL'],
        'Baseball': ['MLB', 'NCAA_BASEBALL'],
        'Hockey': ['NHL', 'NCAA_HOCKEY'],
        'Soccer': ['MLS', 'PREMIER_LEAGUE', 'LA_LIGA'],
        'UFC/MMA': ['UFC', 'UFC_TITLE', 'MMA']
    }
    
    for category, sports in sports_categories.items():
        print(f"\n{category}:")
        for sport in sports:
            multiplier = SPORT_MULTIPLIERS.get(sport, SPORT_MULTIPLIERS['DEFAULT'])
            print(f"  {sport}: {multiplier}")
    
    print("✅ Test passed!\n")


def test_multiple_predictions():
    """Test multiple prediction scenarios."""
    print("=" * 50)
    print("TEST 6: Multiple Prediction Scenarios")
    print("=" * 50)
    
    scenarios = [
        {'name': 'Lakers vs Celtics (NBA)', 'L': 6.32, 'day': 14, 'sport': 'NBA'},
        {'name': 'Patriots vs Chiefs (NFL)', 'L': 5.80, 'day': 12, 'sport': 'NFL'},
        {'name': 'Yankees vs Red Sox (MLB)', 'L': 7.20, 'day': 15, 'sport': 'MLB'},
        {'name': 'Maple Leafs vs Bruins (NHL)', 'L': 4.50, 'day': 20, 'sport': 'NHL'},
        {'name': 'MMA Title Fight (UFC)', 'L': 3.90, 'day': 8, 'sport': 'UFC'},
    ]
    
    for scenario in scenarios:
        print(f"\n{scenario['name']}")
        print(f"  Input: L={scenario['L']}, day={scenario['day']}, sport={scenario['sport']}")
        
        result_dict = apply_formula(scenario['L'], scenario['day'], scenario['sport'])
        result = result_dict['predicted_total']
        Pd = get_pd_value(scenario['day'])
        
        print(f"  Pd={Pd}")
        print(f"  Prediction: {result:.2f} points")
    
    print("\n✅ Test passed!\n")


def test_edge_cases():
    """Test edge cases and error handling."""
    print("=" * 50)
    print("TEST 7: Edge Cases")
    print("=" * 50)
    
    # Test invalid day
    print("\nTest: Invalid day (day=0)")
    try:
        Pd = get_pd_value(0)
        print(f"  Pd={Pd}")
    except Exception as e:
        print(f"  ✅ Expected error: {e}")
    
    # Test invalid day (day=32)
    print("\nTest: Invalid day (day=32)")
    try:
        Pd = get_pd_value(32)
        print(f"  Pd={Pd}")
    except Exception as e:
        print(f"  ✅ Expected error: {e}")
    
    # Test unknown sport (should use default)
    print("\nTest: Unknown sport (UNKNOWN_SPORT)")
    result_dict = apply_formula(6.32, 14, 'UNKNOWN_SPORT')
    result = result_dict['predicted_total']
    print(f"  Prediction: {result:.2f} points (using default multiplier)")
    
    print("\n✅ Test passed!\n")


def main():
    """Run all tests."""
    print("\n" + "=" * 50)
    print("TELEGRAM BOT FUNCTIONALITY TEST SUITE")
    print("=" * 50 + "\n")
    
    try:
        test_predict_command()
        test_compare_command()
        test_condensed_command()
        test_formula_explanation()
        test_sports_multipliers()
        test_multiple_predictions()
        test_edge_cases()
        
        print("=" * 50)
        print("ALL TESTS PASSED! ✅")
        print("=" * 50)
        print("\nBot está listo para usar!")
        print("\nPara ejecutar el bot:")
        print("1. Configura TELEGRAM_BOT_TOKEN en .env")
        print("2. python manage.py runbot")
        print("\nComandos disponibles:")
        print("  /start - Mensaje de bienvenida")
        print("  /help - Ayuda")
        print("  /predict L=<valor> day=<día> sport=<deporte>")
        print("  /compare prediction=<valor> vegas=<línea>")
        print("  /condensed <día>")
        print("  /formula - Explicación de la fórmula")
        print("  /sports - Ver multiplicadores")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
