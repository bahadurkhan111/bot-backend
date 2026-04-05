"""
Business logic service for predictions.
"""
import logging
from typing import Dict, Tuple, Optional
from django.db import transaction
from django.utils import timezone
from .models import Team, Game, Prediction
from apps.models_ml.ensemble import ensemble_predictor

logger = logging.getLogger(__name__)


class PredictionService:
    """
    Service layer for handling prediction business logic.
    """
    
    @staticmethod
    def get_or_create_team(name: str, sport: str = 'NBA') -> Team:
        """
        Get or create a team and ensure gematria values are calculated.
        
        Args:
            name: Team name
            sport: Sport type
            
        Returns:
            Team instance
        """
        team, created = Team.objects.get_or_create(
            name=name,
            defaults={'sport': sport}
        )
        
        if created or not team.gematria_values:
            team.calculate_gematria_values()
            logger.info(f"Created new team: {name}")
        
        return team
    
    @staticmethod
    @transaction.atomic
    def create_prediction(
        team1_name: str,
        team2_name: str,
        sport: str = 'NBA'
    ) -> Optional[Tuple[Prediction, Dict]]:
        """
        Create a complete prediction for a game.
        
        Args:
            team1_name: Name of team1
            team2_name: Name of team2
            sport: Sport type
            
        Returns:
            Tuple of (Prediction instance, response data) or None if failed
        """
        try:
            # Get or create teams
            team1 = PredictionService.get_or_create_team(team1_name, sport)
            team2 = PredictionService.get_or_create_team(team2_name, sport)
            
            # Get gematria values
            team1_gematria = team1.get_gematria_values()
            team2_gematria = team2.get_gematria_values()
            
            # Make ensemble prediction
            result = ensemble_predictor.predict_game(
                team1_gematria,
                team2_gematria,
                team1.name,
                team2.name
            )
            
            if result is None:
                logger.error("Ensemble prediction failed")
                return None

            ensemble_result = result['ensemble_result']
            raw_predictions = result['raw_predictions']
            
            # Create or get game
            game, _ = Game.objects.get_or_create(
                team1=team1,
                team2=team2,
                date=timezone.now(),
                defaults={'status': 'SCHEDULED'}
            )
            
            # Determine predicted winner
            if ensemble_result.predicted_winner_index == 0:
                predicted_winner = team1
            else:
                predicted_winner = team2
            
            # Get model votes — only for models that actually loaded
            model_votes = ensemble_result.model_votes
            vote_mapping = {}
            for model_name in ['lasso', 'xgboost', 'linear', 'model4']:
                if model_name in model_votes:
                    vote_mapping[model_name] = team1 if model_votes[model_name].team_index == 0 else team2

            # Create prediction record
            prediction = Prediction.objects.create(
                game=game,
                predicted_winner=predicted_winner,
                signal=ensemble_result.signal,
                confidence=ensemble_result.confidence,
                model_consensus=ensemble_result.consensus,
                lasso_prediction=raw_predictions.get('lasso', 0.0),
                xgboost_prediction=raw_predictions.get('xgboost', 0.0),
                linear_prediction=raw_predictions.get('linear', 0.0),
                model4_prediction=raw_predictions.get('model4', 0.0),
                lasso_vote=vote_mapping.get('lasso'),
                xgboost_vote=vote_mapping.get('xgboost'),
                linear_vote=vote_mapping.get('linear'),
                model4_vote=vote_mapping.get('model4'),
                feature_vector={
                    'team1_gematria': team1_gematria,
                    'team2_gematria': team2_gematria,
                }
            )

            # Build response data
            model_breakdown = {}
            for model_name in ['lasso', 'xgboost', 'linear', 'model4']:
                if model_name in vote_mapping:
                    model_breakdown[model_name] = {
                        'team': vote_mapping[model_name].name,
                        'probability': raw_predictions.get(model_name, 0.0),
                    }
                else:
                    model_breakdown[model_name] = {
                        'team': 'N/A (model not loaded)',
                        'probability': 0.0,
                    }

            response_data = {
                'predicted_winner': predicted_winner.name,
                'signal': ensemble_result.signal,
                'confidence': ensemble_result.confidence,
                'model_consensus': ensemble_result.consensus,
                'recommendation': prediction.get_recommendation(),
                'model_breakdown': model_breakdown,
                'game_id': game.id,
                'prediction_id': prediction.id,
                'team1': {
                    'id': team1.id,
                    'name': team1.name,
                    'sport': team1.sport,
                },
                'team2': {
                    'id': team2.id,
                    'name': team2.name,
                    'sport': team2.sport,
                },
            }
            
            logger.info(
                f"Created prediction: {team1.name} vs {team2.name} - "
                f"{ensemble_result.signal} ({ensemble_result.confidence:.1f}%)"
            )
            
            return prediction, response_data
            
        except Exception as e:
            logger.error(f"Error creating prediction: {e}", exc_info=True)
            return None
    
    @staticmethod
    def get_prediction_stats() -> Dict:
        """
        Calculate prediction statistics.
        
        Returns:
            Dictionary with various statistics
        """
        from django.db.models import Count, Avg, Q
        
        total = Prediction.objects.count()
        completed = Prediction.objects.filter(was_correct__isnull=False).count()
        correct = Prediction.objects.filter(was_correct=True).count()
        
        # Signal breakdown
        signals = Prediction.objects.values('signal').annotate(count=Count('signal'))
        signal_breakdown = {s['signal']: s['count'] for s in signals}
        
        # Accuracy by signal
        bullish_correct = Prediction.objects.filter(
            signal='BULLISH', was_correct=True
        ).count()
        bullish_total = Prediction.objects.filter(
            signal='BULLISH', was_correct__isnull=False
        ).count()
        
        bearish_correct = Prediction.objects.filter(
            signal='BEARISH', was_correct=True
        ).count()
        bearish_total = Prediction.objects.filter(
            signal='BEARISH', was_correct__isnull=False
        ).count()
        
        neutral_correct = Prediction.objects.filter(
            signal='NEUTRAL', was_correct=True
        ).count()
        neutral_total = Prediction.objects.filter(
            signal='NEUTRAL', was_correct__isnull=False
        ).count()
        
        # Average metrics
        avg_data = Prediction.objects.aggregate(
            avg_confidence=Avg('confidence'),
            avg_consensus=Avg('model_consensus')
        )
        
        return {
            'total_predictions': total,
            'completed_games': completed,
            'correct_predictions': correct,
            'accuracy': (correct / completed * 100) if completed > 0 else 0.0,
            'signal_breakdown': signal_breakdown,
            'bullish_accuracy': (bullish_correct / bullish_total * 100) if bullish_total > 0 else 0.0,
            'bearish_accuracy': (bearish_correct / bearish_total * 100) if bearish_total > 0 else 0.0,
            'neutral_accuracy': (neutral_correct / neutral_total * 100) if neutral_total > 0 else 0.0,
            'avg_confidence': avg_data['avg_confidence'] or 0.0,
            'avg_consensus': avg_data['avg_consensus'] or 0.0,
        }
