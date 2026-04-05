"""
Test the prediction API endpoint

This script demonstrates how to use the prediction system through the API.
"""
import requests
from datetime import date

# Base URL (update if running on different host/port)
BASE_URL = "http://localhost:8000/api"

def test_prediction_api():
    """Test the prediction API endpoint."""
    
    print("=" * 70)
    print("TESTING PREDICTION API")
    print("=" * 70)
    
    # Example prediction request
    payload = {
        "game_date": "2026-01-14",  # January 14, 2026
        "home_team": "Lakers",
        "away_team": "Celtics",
        "sport": "NBA",
        "linear_output": 6.32  # From ML model
    }
    
    print(f"\nRequest payload:")
    print(f"  Date: {payload['game_date']}")
    print(f"  Game: {payload['away_team']} @ {payload['home_team']}")
    print(f"  Sport: {payload['sport']}")
    print(f"  Linear output: {payload['linear_output']}")
    
    try:
        # Make API request
        response = requests.post(
            f"{BASE_URL}/predictions/predict/",
            json=payload,
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "=" * 70)
            print("API RESPONSE:")
            print("=" * 70)
            print(f"\n🎯 Predicted Total: {result['predicted_total']} points")
            print(f"\nFormula Details:")
            print(f"  Day: {result['day_of_month']}")
            print(f"  Pd: {result['pd_value']} ({result.get('sequence', 'N/A')})")
            print(f"  Truest Number: {result['truest_number']}")
            print(f"  Sport Multiplier: {result['sport_multiplier']}")
            
            if 'formula_steps' in result:
                print(f"\nFormula Steps:")
                for step in result['formula_steps']:
                    print(f"  {step}")
        else:
            print(f"\n❌ API Error: {response.status_code}")
            print(f"   {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("\n⚠️  Cannot connect to API. Is the Django server running?")
        print("   Start server with: python manage.py runserver")
    except Exception as e:
        print(f"\n❌ Error: {e}")


def test_batch_predictions():
    """Test multiple predictions."""
    
    print("\n\n" + "=" * 70)
    print("BATCH PREDICTIONS")
    print("=" * 70)
    
    games = [
        {"date": "2026-01-01", "home": "Warriors", "away": "Lakers", "sport": "NBA", "linear": 5.0},
        {"date": "2026-01-07", "home": "Chiefs", "away": "Patriots", "sport": "NFL", "linear": 6.5},
        {"date": "2026-01-14", "home": "Lakers", "away": "Celtics", "sport": "NBA", "linear": 6.32},
        {"date": "2026-01-21", "home": "Red Sox", "away": "Yankees", "sport": "MLB", "linear": 7.8},
    ]
    
    print(f"\n{'Date':<12} {'Game':<25} {'Sport':<6} {'Prediction':<12}")
    print("-" * 70)
    
    for game in games:
        payload = {
            "game_date": game['date'],
            "home_team": game['home'],
            "away_team": game['away'],
            "sport": game['sport'],
            "linear_output": game['linear']
        }
        
        try:
            response = requests.post(
                f"{BASE_URL}/predictions/predict/",
                json=payload,
                timeout=5
            )
            
            if response.status_code == 200:
                result = response.json()
                game_str = f"{game['away']} @ {game['home']}"
                print(f"{game['date']:<12} {game_str:<25} {game['sport']:<6} {result['predicted_total']:>6.2f} points")
            else:
                print(f"{game['date']:<12} ERROR: {response.status_code}")
                
        except requests.exceptions.ConnectionError:
            print(f"{game['date']:<12} ⚠️  Server not running")
            break
        except Exception as e:
            print(f"{game['date']:<12} ERROR: {e}")
    
    print("-" * 70)


if __name__ == '__main__':
    print("\n🔧 NOTE: Make sure Django server is running:")
    print("   python manage.py runserver\n")
    
    test_prediction_api()
    test_batch_predictions()
    
    print("\n\n✅ API tests completed!")
