"""
Pattern Recognition & Loss-Aware Adjustment System

Tracks prediction outcomes, detects patterns, and adjusts
future predictions based on historical accuracy.

Key features:
- Logs every prediction with outcome tracking
- Detects streaks (win/loss), day-of-month patterns, sport-specific accuracy
- Loss-aware adjustment: when predictions are wrong, adjusts the linear
  regression output (L) using a correction factor learned from errors
- Self-correcting: the adjustment factor converges as more data is collected
"""
import json
import logging
import os
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

logger = logging.getLogger(__name__)

# Persistent storage path
DATA_DIR = Path(__file__).parent.parent.parent / 'data' / 'predictions'
PREDICTIONS_FILE = DATA_DIR / 'prediction_log.json'
ADJUSTMENT_FILE = DATA_DIR / 'adjustment_state.json'


class PatternTracker:
    """
    Tracks predictions, detects patterns, and applies loss-aware adjustments.
    """

    def __init__(self):
        self.predictions: List[Dict] = []
        self.adjustment_factor: float = 1.0
        self.correction_history: List[float] = []
        self._load_data()

    def _load_data(self):
        """Load saved prediction data from disk."""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)

            if PREDICTIONS_FILE.exists():
                with open(PREDICTIONS_FILE, 'r') as f:
                    self.predictions = json.load(f)

            if ADJUSTMENT_FILE.exists():
                with open(ADJUSTMENT_FILE, 'r') as f:
                    state = json.load(f)
                    self.adjustment_factor = state.get('adjustment_factor', 1.0)
                    self.correction_history = state.get('correction_history', [])
        except Exception as e:
            logger.error(f"Error loading pattern data: {e}")
            self.predictions = []
            self.adjustment_factor = 1.0

    def _save_data(self):
        """Save prediction data to disk."""
        try:
            os.makedirs(DATA_DIR, exist_ok=True)

            with open(PREDICTIONS_FILE, 'w') as f:
                json.dump(self.predictions, f, indent=2, default=str)

            with open(ADJUSTMENT_FILE, 'w') as f:
                json.dump({
                    'adjustment_factor': self.adjustment_factor,
                    'correction_history': self.correction_history[-100:],
                    'last_updated': str(datetime.now()),
                }, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving pattern data: {e}")

    def log_prediction(
        self,
        sport: str,
        day: int,
        predicted_total: float,
        linear_output: float,
        base_number: int,
        date_digit_sum: int,
        game_date: Optional[str] = None,
        actual_total: Optional[float] = None,
        teams: Optional[str] = None,
    ):
        """
        Log a prediction for pattern tracking.
        """
        entry = {
            'id': len(self.predictions) + 1,
            'timestamp': str(datetime.now()),
            'sport': sport,
            'day_of_month': day,
            'predicted_total': predicted_total,
            'linear_output': linear_output,
            'base_number': base_number,
            'date_digit_sum': date_digit_sum,
            'game_date': game_date,
            'actual_total': actual_total,
            'teams': teams,
            'was_correct': None,
            'error': None,
            'adjustment_applied': self.adjustment_factor,
        }

        self.predictions.append(entry)
        self._save_data()
        logger.info(f"Logged prediction #{entry['id']}: {sport} day={day} predicted={predicted_total:.2f}")

    def record_outcome(self, prediction_id: int, actual_total: float):
        """
        Record the actual outcome for a prediction and update adjustment factor.

        Args:
            prediction_id: ID of the prediction to update
            actual_total: The actual total points from the game
        """
        for pred in self.predictions:
            if pred['id'] == prediction_id:
                pred['actual_total'] = actual_total
                error = actual_total - pred['predicted_total']
                pred['error'] = error

                # Determine if prediction was "correct" (within 15% of actual)
                if actual_total > 0:
                    pct_error = abs(error) / actual_total
                    pred['was_correct'] = pct_error < 0.15
                else:
                    pred['was_correct'] = abs(error) < 10

                # Update loss-aware adjustment
                self._update_adjustment(error, pred['predicted_total'])
                self._save_data()

                logger.info(
                    f"Recorded outcome for prediction #{prediction_id}: "
                    f"predicted={pred['predicted_total']:.2f}, actual={actual_total:.2f}, "
                    f"error={error:.2f}, correct={pred['was_correct']}"
                )
                return True

        return False

    def _update_adjustment(self, error: float, predicted: float):
        """
        Update the loss-aware adjustment factor using exponential moving average.

        When predictions are consistently too high or too low, the adjustment
        factor shifts to compensate. Uses a learning rate that decreases
        as more data is collected (more confident adjustments over time).
        """
        if predicted == 0:
            return

        # Error ratio: how far off we were as a proportion
        error_ratio = error / predicted

        # Store correction
        self.correction_history.append(error_ratio)

        # Learning rate decreases with more data (min 0.01, max 0.2)
        n = len(self.correction_history)
        learning_rate = max(0.01, min(0.2, 1.0 / (n + 5)))

        # Exponential moving average of correction
        # If error is positive (actual > predicted), factor goes up
        # If error is negative (actual < predicted), factor goes down
        self.adjustment_factor = self.adjustment_factor * (1 + learning_rate * error_ratio)

        # Clamp to reasonable range
        self.adjustment_factor = max(0.5, min(2.0, self.adjustment_factor))

        logger.info(
            f"Adjustment factor updated: {self.adjustment_factor:.4f} "
            f"(learning_rate={learning_rate:.4f}, error_ratio={error_ratio:.4f})"
        )

    def get_adjusted_prediction(self, raw_prediction: float) -> float:
        """
        Apply the loss-aware adjustment to a raw prediction.

        Args:
            raw_prediction: The prediction from the base formula

        Returns:
            Adjusted prediction
        """
        return raw_prediction * self.adjustment_factor

    def detect_patterns(self) -> List[Dict]:
        """
        Analyze prediction history and detect patterns.

        Returns:
            List of detected pattern descriptions
        """
        patterns = []

        if len(self.predictions) < 3:
            return patterns

        completed = [p for p in self.predictions if p['was_correct'] is not None]
        if not completed:
            return patterns

        # Pattern 1: Day-of-month accuracy
        day_stats = defaultdict(lambda: {'correct': 0, 'total': 0})
        for p in completed:
            day = p['day_of_month']
            day_stats[day]['total'] += 1
            if p['was_correct']:
                day_stats[day]['correct'] += 1

        for day, stats in day_stats.items():
            if stats['total'] >= 3:
                accuracy = stats['correct'] / stats['total'] * 100
                if accuracy >= 75:
                    patterns.append({
                        'type': 'day_strength',
                        'description': f"Day {day} is a strong prediction day ({accuracy:.0f}% accuracy, {stats['total']} games)",
                        'confidence': accuracy,
                        'day': day,
                    })
                elif accuracy <= 25:
                    patterns.append({
                        'type': 'day_weakness',
                        'description': f"Day {day} is weak for predictions ({accuracy:.0f}% accuracy) - consider extra caution",
                        'confidence': accuracy,
                        'day': day,
                    })

        # Pattern 2: Sport-specific accuracy
        sport_stats = defaultdict(lambda: {'correct': 0, 'total': 0, 'errors': []})
        for p in completed:
            sport = p['sport']
            sport_stats[sport]['total'] += 1
            if p['was_correct']:
                sport_stats[sport]['correct'] += 1
            if p.get('error') is not None:
                sport_stats[sport]['errors'].append(p['error'])

        for sport, stats in sport_stats.items():
            if stats['total'] >= 3:
                accuracy = stats['correct'] / stats['total'] * 100
                avg_error = sum(stats['errors']) / len(stats['errors']) if stats['errors'] else 0
                patterns.append({
                    'type': 'sport_accuracy',
                    'description': f"{sport}: {accuracy:.0f}% accuracy ({stats['total']} predictions, avg error: {avg_error:+.1f})",
                    'confidence': accuracy,
                    'sport': sport,
                    'avg_error': avg_error,
                })

        # Pattern 3: Streak detection
        recent = completed[-20:]
        if len(recent) >= 3:
            streak_type = recent[-1]['was_correct']
            streak_len = 1
            for p in reversed(recent[:-1]):
                if p['was_correct'] == streak_type:
                    streak_len += 1
                else:
                    break

            if streak_len >= 3:
                streak_word = "winning" if streak_type else "losing"
                patterns.append({
                    'type': 'streak',
                    'description': f"Current {streak_word} streak: {streak_len} predictions in a row",
                    'streak_length': streak_len,
                    'is_winning': streak_type,
                })

        # Pattern 4: Over/Under bias
        errors = [p['error'] for p in completed if p.get('error') is not None]
        if len(errors) >= 5:
            avg_error = sum(errors) / len(errors)
            if avg_error > 5:
                patterns.append({
                    'type': 'bias',
                    'description': f"Predictions tend to be LOW by {avg_error:.1f} points on average - adjustment factor active",
                    'avg_error': avg_error,
                })
            elif avg_error < -5:
                patterns.append({
                    'type': 'bias',
                    'description': f"Predictions tend to be HIGH by {abs(avg_error):.1f} points on average - adjustment factor active",
                    'avg_error': avg_error,
                })

        # Pattern 5: Base number correlation
        base_stats = defaultdict(lambda: {'errors': [], 'correct': 0, 'total': 0})
        for p in completed:
            bn = p.get('base_number', 0)
            base_stats[bn]['total'] += 1
            if p['was_correct']:
                base_stats[bn]['correct'] += 1
            if p.get('error') is not None:
                base_stats[bn]['errors'].append(p['error'])

        for bn, stats in base_stats.items():
            if stats['total'] >= 3:
                accuracy = stats['correct'] / stats['total'] * 100
                if accuracy >= 80:
                    patterns.append({
                        'type': 'base_number',
                        'description': f"Base Number {bn} correlates with high accuracy ({accuracy:.0f}%)",
                        'base_number': bn,
                    })

        return patterns

    def get_patterns_summary(self) -> Dict:
        """Get a summary of all detected patterns."""
        completed = [p for p in self.predictions if p['was_correct'] is not None]
        correct = sum(1 for p in completed if p['was_correct'])
        accuracy = (correct / len(completed) * 100) if completed else 0.0

        return {
            'total_predictions': len(self.predictions),
            'completed': len(completed),
            'accuracy_rate': accuracy,
            'adjustment_factor': self.adjustment_factor,
            'loss_adjustment_active': abs(self.adjustment_factor - 1.0) > 0.01,
            'patterns': self.detect_patterns(),
        }

    def get_accuracy_stats(self) -> Dict:
        """Get detailed accuracy statistics."""
        completed = [p for p in self.predictions if p['was_correct'] is not None]
        correct = sum(1 for p in completed if p['was_correct'])
        incorrect = len(completed) - correct
        pending = len(self.predictions) - len(completed)

        # By sport
        sport_breakdown = defaultdict(lambda: {'correct': 0, 'total': 0})
        for p in completed:
            sport = p['sport']
            sport_breakdown[sport]['total'] += 1
            if p['was_correct']:
                sport_breakdown[sport]['correct'] += 1

        by_sport = {}
        for sport, stats in sport_breakdown.items():
            by_sport[sport] = {
                'total': stats['total'],
                'correct': stats['correct'],
                'accuracy': (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0,
            }

        # Streak
        streak = "N/A"
        if completed:
            streak_type = completed[-1]['was_correct']
            streak_len = 1
            for p in reversed(completed[:-1]):
                if p['was_correct'] == streak_type:
                    streak_len += 1
                else:
                    break
            streak = f"{'W' if streak_type else 'L'}{streak_len}"

        return {
            'total': len(self.predictions),
            'correct': correct,
            'incorrect': incorrect,
            'pending': pending,
            'accuracy': (correct / len(completed) * 100) if completed else 0.0,
            'by_sport': by_sport,
            'adjustment_factor': self.adjustment_factor,
            'streak': streak,
        }


# Global instance
pattern_tracker = PatternTracker()
