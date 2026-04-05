"""
Formula Utilities for Sports Prediction

Implements the client's prediction formula:
T = ((Base_Number + L + Date_Digit_Sum) / 2) × 4

Where:
- L = Linear Regression model output  
- Base_Number = Calculated from day properties (geometric shapes + numeric sequences)
- Date_Digit_Sum = Sum of all individual digits in the date (MM/DD/YYYY)
  Example: 01/14/2026 → 0+1+1+4+2+0+2+6 = 16
- Geometric shapes are multiplied by their sides/faces
- Numeric sequences (Prime, Fibonacci) are kept as position numbers
- Multiple properties: multiply shapes by sides, add all together
"""

from decimal import Decimal
from typing import Dict, Tuple, Optional, List
from datetime import date
import pandas as pd
from pathlib import Path
import os


# Geometric shape sides/faces mapping
SHAPE_SIDES = {
    'Triangular': 3,
    'Square': 4,
    'Tetrahedral': 4,
    'Pentagonal': 5,
    'Square Pyramidal': 5,
    'Star': 5,
    'Cube': 6,
}

# Numeric sequences that DON'T have geometric interpretation
NUMERIC_SEQUENCES = ['Prime', 'Fibonacci', 'Composite']

# Sport multipliers (currently not used, formula uses × 4 for all)
SPORT_MULTIPLIERS = {
    # Basketball (4 quarters)
    'NBA': 1.15,
    'WNBA': 1.15,
    'NCAA_BASKETBALL': 1.15,
    'EUROLEAGUE': 1.15,
    'BASKETBALL': 1.15,
    
    # Football (4 quarters)
    'NFL': 1.06,
    'NCAA_FOOTBALL': 1.06,
    'FOOTBALL': 1.06,
    
    # Baseball (9 innings)
    'MLB': 0.90,
    'NCAA_BASEBALL': 0.90,
    'BASEBALL': 0.90,
    
    # Hockey (3 periods)
    'NHL': 1.20,
    'NCAA_HOCKEY': 1.20,
    'HOCKEY': 1.20,
    
    # Soccer (2 halves)
    'MLS': 1.10,
    'PREMIER_LEAGUE': 1.10,
    'LA_LIGA': 1.10,
    'SERIE_A': 1.10,
    'BUNDESLIGA': 1.10,
    'LIGUE_1': 1.10,
    'CHAMPIONS_LEAGUE': 1.10,
    'WORLD_CUP': 1.10,
    'SOCCER': 1.10,
    
    # UFC/MMA
    'UFC': 1.25,
    'UFC_TITLE': 1.25,
    'UFC_MAIN_EVENT': 1.25,
    'MMA': 1.25,
    
    # Default
    'DEFAULT': 1.15,
}


def calculate_date_digit_sum(game_date: date) -> int:
    """
    Calculate Date Digit Sum (Numerology #3 from Date Calculator).
    
    Sums all individual digits from the date in MM/DD/YYYY format.
    
    Algorithm:
    1. Format date as MM/DD/YYYY
    2. Extract each digit: M1, M2, D1, D2, Y1, Y2, Y3, Y4
    3. Sum all 8 digits
    
    Examples:
        01/14/2026 → 0+1+1+4+2+0+2+6 = 16
        01/15/2026 → 0+1+1+5+2+0+2+6 = 17
        12/31/2025 → 1+2+3+1+2+0+2+5 = 16
        
    Args:
        game_date: Date object for the game
        
    Returns:
        Sum of all date digits (typically 10-40)
    """
    # Convert string to date if needed
    if isinstance(game_date, str):
        from datetime import datetime
        game_date = datetime.strptime(game_date, '%Y-%m-%d').date()

    # Format as MM/DD/YYYY
    month = f"{game_date.month:02d}"
    day = f"{game_date.day:02d}"
    year = f"{game_date.year:04d}"
    
    # Sum all individual digits
    date_string = month + day + year
    digit_sum = sum(int(digit) for digit in date_string)
    
    return digit_sum


def numerological_reduction(value: float) -> int:
    """
    Reduce any number to single digit by summing digits repeatedly.
    This is the core numerological transformation.
    
    Algorithm:
    1. Remove decimal point and convert to string
    2. Sum all individual digits
    3. If result >= 10, repeat until single digit (1-9)
    
    Examples:
        15.66 → digits: [1,5,6,6] → sum: 18 → 1+8 → 9
        31.32 → digits: [3,1,3,2] → sum: 9
        123.45 → digits: [1,2,3,4,5] → sum: 15 → 1+5 → 6
        0.5 → digits: [0,5] → sum: 5
        
    Args:
        value: Any numeric value (int or float)
        
    Returns:
        Single digit from 1-9
    """
    # Convert to string and remove decimal point
    str_value = str(abs(value)).replace('.', '').replace('-', '')
    
    # Extract all digits
    digits = [int(d) for d in str_value if d.isdigit()]
    
    # Sum digits
    total = sum(digits)
    
    # Reduce until single digit
    while total >= 10:
        total = sum(int(d) for d in str(total))
    
    # Ensure we return at least 1 (not 0)
    return max(total, 1)


def get_sport_multiplier(sport: str) -> float:
    """
    Get the sport multiplier for a given sport.
    
    Args:
        sport: Sport name/code (case-insensitive)
        
    Returns:
        Float multiplier (e.g., 1.15 for Basketball, 1.06 for Football)
    """
    sport_upper = sport.upper().strip()
    return SPORT_MULTIPLIERS.get(sport_upper, SPORT_MULTIPLIERS['DEFAULT'])


def get_base_number_from_csv(day_of_month: int) -> Tuple[int, str, List[Dict]]:
    """
    Calculate Base_Number for a given day based on geometric shapes and numeric sequences.
    
    Rules:
    1. Geometric shapes (Triangular, Square, Cube, etc.) are multiplied by their sides/faces
    2. Numeric sequences (Prime, Fibonacci) are kept as their position number
    3. If multiple properties: multiply each shape by sides, add all numbers together
    4. If only numeric sequences without shapes: concatenate positions
    
    Examples:
        Day 29: 10th Prime → Base = 10
        Day 2: 1st Prime + 3rd Fibonacci → Base = 13 (concatenate "1" + "3")
        Day 21: 8th Fibonacci + 6th Triangular → Base = (6×3) + 8 = 26
        Day 5: 3rd Prime + 5th Fibonacci + 2nd Sq.Pyr + 2nd Penta → Base = (2×5) + (2×5) + 3 + 5 = 28
        Day 1: Multiple shapes → Base = 1 + (1×3) + (1×4) + (1×6) + (1×4) + (1×5) + (1×5) + (1×5) = 33
    
    Args:
        day_of_month: Day of the month (1-31)
        
    Returns:
        Tuple of (base_number, calculation_explanation, properties_list)
    """
    # Special case: Day 1 has all 8 properties (CSV is incomplete)
    if day_of_month == 1:
        calculation = "1 (Fibonacci) + 1×3 (Triangular) + 1×4 (Square) + 1×6 (Cube) + 1×4 (Tetrahedral) + 1×5 (Sq.Pyramidal) + 1×5 (Star) + 1×5 (Pentagonal) = 33"
        properties = [
            {'position': 1, 'sequence': 'Fibonacci', 'is_shape': False, 'sides': None},
            {'position': 1, 'sequence': 'Triangular', 'is_shape': True, 'sides': 3},
            {'position': 1, 'sequence': 'Square', 'is_shape': True, 'sides': 4},
            {'position': 1, 'sequence': 'Cube', 'is_shape': True, 'sides': 6},
            {'position': 1, 'sequence': 'Tetrahedral', 'is_shape': True, 'sides': 4},
            {'position': 1, 'sequence': 'Square Pyramidal', 'is_shape': True, 'sides': 5},
            {'position': 1, 'sequence': 'Star', 'is_shape': True, 'sides': 5},
            {'position': 1, 'sequence': 'Pentagonal', 'is_shape': True, 'sides': 5},
        ]
        return 33, calculation, properties
    
    # Path to CSV with properties
    csv_path = Path(__file__).parent.parent.parent / 'data' / 'gematrinator_output' / 'condensed_numbers_with_pd.csv'
    
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Properties CSV not found at {csv_path}. "
            "Run scripts/gematrinator_scraper/ first."
        )
    
    # Load CSV
    df = pd.read_csv(csv_path)
    row = df[df['number'] == day_of_month]
    
    if row.empty:
        raise ValueError(f"No properties found for day {day_of_month}")
    
    row = row.iloc[0]
    
    # Extract all properties
    properties = []
    for i in range(1, 6):  # Up to 5 properties
        pos_col = f'position_{i}'
        seq_col = f'sequence_{i}'
        
        if pd.notna(row.get(pos_col)) and pd.notna(row.get(seq_col)):
            position = int(row[pos_col])
            sequence = str(row[seq_col])
            properties.append({
                'position': position,
                'sequence': sequence,
                'is_shape': sequence in SHAPE_SIDES,
                'sides': SHAPE_SIDES.get(sequence, None)
            })
    
    # Handle case with no highlighted properties (fallback)


    # Handle case with no highlighted properties (fallback)
    if len(properties) == 0:
        # Use Pd value from CSV for days with no properties (18, 24, 26)
        pd_value = int(row['Pd'])
        return pd_value, f"Fallback Pd value = {pd_value}", []
    
    # Separate shapes and numeric sequences
    shapes = [p for p in properties if p['is_shape']]
    numerics = [p for p in properties if not p['is_shape']]
    
    # Calculate base number
    calculation_parts = []
    total = 0
    
    # Case 1: Only numeric sequences (no shapes) → Concatenate
    if len(shapes) == 0 and len(numerics) > 0:
        if len(numerics) == 1:
            # Single numeric property
            base_number = numerics[0]['position']
            calculation = f"{numerics[0]['position']} ({numerics[0]['sequence']})"
        else:
            # Multiple numeric properties → concatenate positions
            concat_str = ''.join(str(n['position']) for n in numerics)
            base_number = int(concat_str)
            parts = [f"{n['position']}({n['sequence']})" for n in numerics]
            calculation = f"Concatenate: {' + '.join(parts)} = {concat_str}"
    
    # Case 2: Has shapes (with or without numerics)
    else:
        components = []
        
        # Add numeric sequences as-is
        for num in numerics:
            total += num['position']
            components.append(f"{num['position']} ({num['sequence']})")
            calculation_parts.append(str(num['position']))
        
        # Multiply shapes by their sides/faces
        for shape in shapes:
            shape_value = shape['position'] * shape['sides']
            total += shape_value
            components.append(f"{shape['position']}×{shape['sides']} ({shape['sequence']})")
            calculation_parts.append(f"{shape['position']}×{shape['sides']}={shape_value}")
        
        base_number = total
        calculation = ' + '.join(calculation_parts) + f" = {base_number}"
        if components:
            calculation = ' + '.join(components) + f" = {base_number}"
    
    return base_number, calculation, properties


def get_pd_value(day_of_month: int) -> Optional[int]:
    """
    Get the condensed Pd value for a given day of the month.
    This is the Base_Number calculated from geometric properties.

    Args:
        day_of_month: Day of the month (1-31)

    Returns:
        Base number (Pd value) for the day, or None if unavailable
    """
    try:
        base_number, _, _ = get_base_number_from_csv(day_of_month)
        return base_number
    except (FileNotFoundError, ValueError) as e:
        logging.getLogger(__name__).error(f"Error getting Pd value for day {day_of_month}: {e}")
        return None


def calculate_intermediate_value(
    linear_output: float,
    base_number: int
) -> float:
    """
    Calculate the intermediate value: (Base_Number + L) / 2
    
    Args:
        linear_output: Output from Linear Regression model
        base_number: Calculated base number for the day
        
    Returns:
        Intermediate value before final multiplication
    """
    return (base_number + linear_output) / 2


def apply_formula(
    linear_output: float,
    day_of_month: int,
    game_date: Optional[date] = None,
    sport: str = 'NBA',
    base_number: Optional[int] = None
) -> Dict:
    """
    Apply the complete prediction formula.
    
    Formula: T = ((Base_Number + L + Date_Digit_Sum) / 2) × 4
    
    Where:
    - Base_Number is calculated from day properties:
      * Geometric shapes multiplied by sides/faces
      * Numeric sequences added as-is
      * Pure numerics concatenated if no shapes
    - L is Linear Regression output
    - Date_Digit_Sum is sum of all date digits (MM/DD/YYYY)
    - × 4 is fixed multiplier (currently same for all sports)
    
    Args:
        linear_output: Output from Linear Regression model
        day_of_month: Day of the month (1-31)
        game_date: Date object for the game (optional, for Date_Digit_Sum)
        sport: Sport name/code (default: 'NBA')
        base_number: Base number for that day (if None, calculates from CSV)
        
    Returns:
        Dictionary with all formula components and result:
        {
            'linear_output': float,
            'day_of_month': int,
            'base_number': int,
            'base_calculation': str,
            'properties': list,
            'date_digit_sum': int,
            'game_date': str,
            'step_1_sum': float,
            'step_2_divide': float,
            'step_3_multiply': float,
            'sport': str,
            'sport_multiplier': float,
            'predicted_total': float,
            'formula_steps': [...],
            'formula_latex': str
        }
    """
    # Get base number from CSV if not provided
    if base_number is None:
        base_number, base_calculation, properties = get_base_number_from_csv(day_of_month)
    else:
        base_calculation = str(base_number)
        properties = []
    
    # Calculate Date Digit Sum if game_date provided
    date_digit_sum = 0
    if game_date:
        date_digit_sum = calculate_date_digit_sum(game_date)
    
    # Step 1: Add base_number + L + Date_Digit_Sum
    step_1_sum = base_number + linear_output + date_digit_sum
    
    # Step 2: Divide by 2
    step_2_divide = step_1_sum / 2
    
    # Step 3: Multiply by 4 (fixed multiplier)
    step_3_multiply = step_2_divide * 4
    
    # Final result
    predicted_total = round(step_3_multiply, 2)
    
    # Sport multiplier (kept for compatibility, but currently not used in formula)
    sport_multiplier = get_sport_multiplier(sport)
    
    # Build formula steps for transparency
    if game_date:
        if isinstance(game_date, str):
            date_info = f" (from {game_date})"
        else:
            date_info = f" (from {game_date.strftime('%m/%d/%Y')})"
    else:
        date_info = " (not provided)"
    formula_steps = [
        f"Step 1: Linear model output (L) = {linear_output:.2f}",
        f"Step 2: Day of month = {day_of_month}",
        f"Step 3: Base_Number = {base_number} ({base_calculation})",
        f"Step 4: Date_Digit_Sum = {date_digit_sum}{date_info}",
        f"Step 5: Sum = Base_Number + L + Date_Digit_Sum = {base_number} + {linear_output:.2f} + {date_digit_sum} = {step_1_sum:.2f}",
        f"Step 6: Divide by 2 = {step_1_sum:.2f} / 2 = {step_2_divide:.2f}",
        f"Step 7: Multiply by 4 = {step_2_divide:.2f} × 4 = {step_3_multiply:.2f}",
        f"Step 8: Predicted total = {predicted_total:.2f}",
    ]
    
    # LaTeX formula
    formula_latex = f"T({day_of_month}, {sport}) = (({base_number} + {linear_output:.2f} + {date_digit_sum}) / 2) × 4 = {predicted_total}"
    
    return {
        'linear_output': linear_output,
        'day_of_month': day_of_month,
        'base_number': base_number,
        'base_calculation': base_calculation,
        'properties': properties,
        'date_digit_sum': date_digit_sum,
        'game_date': (game_date if isinstance(game_date, str) else game_date.strftime('%Y-%m-%d')) if game_date else None,
        'step_1_sum': round(step_1_sum, 2),
        'step_2_divide': round(step_2_divide, 2),
        'step_3_multiply': round(step_3_multiply, 2),
        'sport': sport,
        'sport_multiplier': sport_multiplier,  # Kept for compatibility
        'predicted_total': predicted_total,
        'formula_steps': formula_steps,
        'formula_latex': formula_latex,
    }


def calculate_prediction_breakdown(
    linear_output: float,
    day_of_month: int,
    base_number: Optional[int] = None,
    sport: str = 'NBA'
) -> Tuple[float, Dict]:
    """
    Calculate prediction and return both the total and detailed breakdown.
    
    This is the main function to use for predictions.
    
    Args:
        linear_output: Output from Linear Regression model
        day_of_month: Day of the month (1-31)
        base_number: Base number for that day (if None, loads from CSV)
        sport: Sport name/code (default: 'NBA')
        
    Returns:
        Tuple of (predicted_total, breakdown_dict)
    """
    breakdown = apply_formula(
        linear_output=linear_output,
        day_of_month=day_of_month,
        base_number=base_number,
        sport=sport
    )
    
    return breakdown['predicted_total'], breakdown


# Example usage for testing
if __name__ == '__main__':
    # Test with confirmed examples from client
    print("=" * 70)
    print("FORMULA TESTS - Confirmed Cases")
    print("=" * 70)
    
    test_cases = [
        (1, 33, 78.64, "All 8 properties: Fibonacci + shapes"),
        (2, 13, 38.64, "1st Prime + 3rd Fibonacci → concatenate"),
        (5, 28, 68.64, "3rd Prime + 5th Fibonacci + 2×Sq.Pyr + 2×Penta"),
        (21, 26, 64.64, "8th Fibonacci + 6th Triangular (6×3)"),
        (29, 10, 32.64, "10th Prime"),
    ]
    
    all_pass = True
    for day, expected_base, expected_result, description in test_cases:
        result = apply_formula(linear_output=6.32, day_of_month=day, sport='NBA')
        
        base_ok = result['base_number'] == expected_base
        result_ok = abs(result['predicted_total'] - expected_result) < 0.01
        
        status = "✅" if (base_ok and result_ok) else "❌"
        print(f"\n{status} Day {day}: {description}")
        print(f"   Base: {result['base_number']} (expected {expected_base}) {'✓' if base_ok else '✗'}")
        print(f"   Result: {result['predicted_total']} (expected {expected_result}) {'✓' if result_ok else '✗'}")
        
        if not (base_ok and result_ok):
            all_pass = False
            print(f"   Calculation: {result['base_calculation']}")
    
    print("\n" + "=" * 70)
    if all_pass:
        print("✅ ALL TESTS PASSED!")
    else:
        print("❌ SOME TESTS FAILED - Review logic")
    print("=" * 70)
