"""
Django models for sports predictions system.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)


class Team(models.Model):
    """
    Represents a sports team.
    """
    SPORT_CHOICES = [
        ('NBA', 'Basketball - NBA'),
        ('NFL', 'Football - NFL'),
        ('MLB', 'Baseball - MLB'),
        ('NHL', 'Hockey - NHL'),
        ('SOCCER', 'Soccer'),
        ('OTHER', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True, db_index=True)
    sport = models.CharField(max_length=50, choices=SPORT_CHOICES, db_index=True)
    gematria_values = models.JSONField(
        default=dict,
        help_text="Cached gematria values for all calculators"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        indexes = [
            models.Index(fields=['name', 'sport']),
        ]
    
    def __str__(self) -> str:
        return f"{self.name} ({self.sport})"
    
    def calculate_gematria_values(self) -> dict:
        """
        Calculate and cache all gematria values for this team.
        
        Returns:
            Dictionary of calculator_name: value pairs
        """
        from apps.calculators.registry import CalculatorRegistry
        
        values = CalculatorRegistry.calculate_all(self.name)
        self.gematria_values = values
        self.save(update_fields=['gematria_values', 'updated_at'])
        logger.info(f"Calculated gematria values for team: {self.name}")
        return values
    
    def get_gematria_values(self) -> dict:
        """
        Get cached gematria values or calculate if not cached.
        
        Returns:
            Dictionary of gematria values
        """
        if not self.gematria_values:
            return self.calculate_gematria_values()
        return self.gematria_values


class Game(models.Model):
    """
    Represents a sports game/match between two teams.
    """
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    team1 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='games_as_team1'
    )
    team2 = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='games_as_team2'
    )
    date = models.DateTimeField(db_index=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='SCHEDULED',
        db_index=True
    )
    actual_winner = models.ForeignKey(
        Team,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='games_won',
        help_text="Actual winner after game completion"
    )
    team1_score = models.IntegerField(null=True, blank=True)
    team2_score = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name = 'Game'
        verbose_name_plural = 'Games'
        indexes = [
            models.Index(fields=['-date', 'status']),
            models.Index(fields=['team1', 'team2', 'date']),
        ]
        constraints = [
            models.CheckConstraint(
                check=~models.Q(team1=models.F('team2')),
                name='different_teams'
            )
        ]
    
    def __str__(self) -> str:
        return f"{self.team1.name} vs {self.team2.name} - {self.date.strftime('%Y-%m-%d')}"
    
    def mark_complete(self, winner: Team, team1_score: int = None, team2_score: int = None) -> None:
        """
        Mark the game as completed with results.
        
        Args:
            winner: Team that won the game
            team1_score: Score for team1 (optional)
            team2_score: Score for team2 (optional)
        """
        if winner not in [self.team1, self.team2]:
            raise ValueError("Winner must be one of the teams in this game")
        
        self.status = 'COMPLETED'
        self.actual_winner = winner
        if team1_score is not None:
            self.team1_score = team1_score
        if team2_score is not None:
            self.team2_score = team2_score
        self.save()
        
        # Update prediction accuracy
        predictions = self.predictions.all()
        for prediction in predictions:
            prediction.update_accuracy()
        
        logger.info(f"Game marked complete: {self} - Winner: {winner.name}")


class Prediction(models.Model):
    """
    Represents a prediction for a game using ML ensemble models.
    """
    SIGNAL_CHOICES = [
        ('BULLISH', 'Bullish - Strong recommendation'),
        ('BEARISH', 'Bearish - Weak confidence'),
        ('NEUTRAL', 'Neutral - No clear consensus'),
    ]
    
    game = models.ForeignKey(
        Game,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    predicted_winner = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='predictions_won'
    )
    signal = models.CharField(
        max_length=20,
        choices=SIGNAL_CHOICES,
        db_index=True
    )
    confidence = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Confidence score 0-100%"
    )
    model_consensus = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Percentage of models that agree"
    )
    
    # Individual model predictions
    lasso_prediction = models.FloatField(
        help_text="Lasso model probability (0-1)"
    )
    xgboost_prediction = models.FloatField(
        help_text="XGBoost model probability (0-1)"
    )
    linear_prediction = models.FloatField(
        help_text="Linear Regression model probability (0-1)"
    )
    model4_prediction = models.FloatField(
        help_text="Model 4 probability (0-1)"
    )
    
    # Individual model votes
    lasso_vote = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='lasso_votes',
        null=True
    )
    xgboost_vote = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='xgboost_votes',
        null=True
    )
    linear_vote = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='linear_votes',
        null=True
    )
    model4_vote = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='model4_votes',
        null=True
    )
    
    # Feature vector used for prediction
    feature_vector = models.JSONField(
        default=dict,
        help_text="Gematria features used for prediction"
    )
    
    # Accuracy tracking
    was_correct = models.BooleanField(
        null=True,
        blank=True,
        help_text="True if prediction matched actual outcome"
    )
    
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Prediction'
        verbose_name_plural = 'Predictions'
        indexes = [
            models.Index(fields=['-created_at', 'signal']),
            models.Index(fields=['game', '-created_at']),
        ]
    
    def __str__(self) -> str:
        return f"Prediction: {self.predicted_winner.name} - {self.signal} ({self.confidence:.1f}%)"
    
    def update_accuracy(self) -> None:
        """
        Update the accuracy field based on actual game outcome.
        Should be called after game is completed.
        """
        if self.game.status == 'COMPLETED' and self.game.actual_winner:
            self.was_correct = (self.predicted_winner == self.game.actual_winner)
            self.save(update_fields=['was_correct', 'updated_at'])
            logger.info(
                f"Updated prediction accuracy: {self} - "
                f"Correct: {self.was_correct}"
            )
    
    def get_recommendation(self) -> str:
        """
        Get betting recommendation based on signal and confidence.
        
        Returns:
            Human-readable recommendation string
        """
        if self.signal == 'BULLISH' and self.confidence >= 75:
            return "Strongly recommended bet - High confidence and consensus"
        elif self.signal == 'BULLISH' and self.confidence >= 60:
            return "Recommended bet - Good confidence"
        elif self.signal == 'BEARISH':
            return "Not recommended - Low confidence despite consensus"
        elif self.signal == 'NEUTRAL':
            return "No recommendation - Models disagree or uncertain"
        else:
            return "Moderate confidence - Consider other factors"
    
    @property
    def model_breakdown(self) -> dict:
        """
        Get detailed breakdown of all model predictions.
        
        Returns:
            Dictionary with model predictions and votes
        """
        return {
            'lasso': {
                'probability': self.lasso_prediction,
                'vote': self.lasso_vote.name if self.lasso_vote else None,
            },
            'xgboost': {
                'probability': self.xgboost_prediction,
                'vote': self.xgboost_vote.name if self.xgboost_vote else None,
            },
            'linear': {
                'probability': self.linear_prediction,
                'vote': self.linear_vote.name if self.linear_vote else None,
            },
            'model4': {
                'probability': self.model4_prediction,
                'vote': self.model4_vote.name if self.model4_vote else None,
            },
        }
