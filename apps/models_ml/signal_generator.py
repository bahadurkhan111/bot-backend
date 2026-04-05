"""
Signal generator for betting recommendations.
Determines BULLISH/BEARISH/NEUTRAL signals based on model consensus.
"""
import logging
from typing import Dict, Tuple
from dataclasses import dataclass
from django.conf import settings

logger = logging.getLogger(__name__)


@dataclass
class ModelVote:
    """Represents a single model's vote and confidence."""
    team_index: int  # 0 or 1 (team1 or team2)
    probability: float  # 0-1
    team_name: str


@dataclass
class EnsembleResult:
    """Result from ensemble prediction."""
    predicted_winner_index: int  # 0 or 1
    predicted_winner_name: str
    signal: str  # BULLISH, BEARISH, or NEUTRAL
    confidence: float  # 0-100
    consensus: float  # 0-100 (percentage of models agreeing)
    model_votes: Dict[str, ModelVote]
    average_probability: float


class SignalGenerator:
    """
    Generates betting signals based on ML model ensemble predictions.
    
    Signal Logic:
    - BULLISH: >= 75% models agree AND avg confidence >= 0.55
    - BEARISH: >= 75% models agree BUT avg confidence < 0.45
    - NEUTRAL: Models disagree OR confidence between 0.45-0.55
    """
    
    def __init__(self):
        """Initialize signal generator with config from settings."""
        self.consensus_threshold = settings.ENSEMBLE_CONFIG['consensus_threshold']
        self.bullish_threshold = settings.ENSEMBLE_CONFIG['bullish_confidence_threshold']
        self.bearish_threshold = settings.ENSEMBLE_CONFIG['bearish_confidence_threshold']
    
    def generate_signal(
        self,
        model_predictions: Dict[str, float],
        team1_name: str,
        team2_name: str
    ) -> EnsembleResult:
        """
        Generate betting signal from model predictions.
        
        Args:
            model_predictions: Dict of model_name -> probability for team1
                              (e.g., {'lasso': 0.87, 'xgboost': 0.92, ...})
            team1_name: Name of team1
            team2_name: Name of team2
            
        Returns:
            EnsembleResult with prediction and signal
        """
        # Convert probabilities to votes
        model_votes = self._calculate_votes(
            model_predictions,
            team1_name,
            team2_name
        )
        
        # Calculate consensus
        consensus = self._calculate_consensus(model_votes)
        
        # Determine predicted winner
        winner_index, avg_probability = self._determine_winner(model_votes)
        winner_name = team1_name if winner_index == 0 else team2_name
        
        # Generate signal
        signal = self._generate_signal(consensus, avg_probability)
        
        # Calculate confidence score (0-100)
        confidence = self._calculate_confidence(consensus, avg_probability)
        
        result = EnsembleResult(
            predicted_winner_index=winner_index,
            predicted_winner_name=winner_name,
            signal=signal,
            confidence=confidence,
            consensus=consensus * 100,  # Convert to percentage
            model_votes=model_votes,
            average_probability=avg_probability
        )
        
        logger.info(
            f"Signal generated: {winner_name} - {signal} "
            f"(confidence: {confidence:.1f}%, consensus: {consensus*100:.1f}%)"
        )
        
        return result
    
    def _calculate_votes(
        self,
        predictions: Dict[str, float],
        team1_name: str,
        team2_name: str
    ) -> Dict[str, ModelVote]:
        """
        Convert model probabilities to discrete votes.
        
        Args:
            predictions: Model predictions (probability for team1)
            team1_name: Team1 name
            team2_name: Team2 name
            
        Returns:
            Dictionary of model votes
        """
        votes = {}
        for model_name, prob_team1 in predictions.items():
            # Model votes for team with higher probability
            if prob_team1 >= 0.5:
                votes[model_name] = ModelVote(
                    team_index=0,
                    probability=prob_team1,
                    team_name=team1_name
                )
            else:
                votes[model_name] = ModelVote(
                    team_index=1,
                    probability=1 - prob_team1,
                    team_name=team2_name
                )
        
        return votes
    
    def _calculate_consensus(self, votes: Dict[str, ModelVote]) -> float:
        """
        Calculate consensus percentage (0-1).
        
        Args:
            votes: Model votes
            
        Returns:
            Consensus as float 0-1
        """
        if not votes:
            return 0.0
        
        # Count votes for each team
        team0_votes = sum(1 for v in votes.values() if v.team_index == 0)
        team1_votes = sum(1 for v in votes.values() if v.team_index == 1)
        
        total_votes = len(votes)
        max_votes = max(team0_votes, team1_votes)
        
        consensus = max_votes / total_votes
        return consensus
    
    def _determine_winner(
        self,
        votes: Dict[str, ModelVote]
    ) -> Tuple[int, float]:
        """
        Determine predicted winner and average probability.
        
        Args:
            votes: Model votes
            
        Returns:
            Tuple of (winner_index, average_probability)
        """
        if not votes:
            return 0, 0.5
        
        # Count votes and sum probabilities
        team0_votes = [v for v in votes.values() if v.team_index == 0]
        team1_votes = [v for v in votes.values() if v.team_index == 1]
        
        # Winner is team with most votes
        if len(team0_votes) >= len(team1_votes):
            winner_index = 0
            avg_prob = sum(v.probability for v in team0_votes) / len(team0_votes)
        else:
            winner_index = 1
            avg_prob = sum(v.probability for v in team1_votes) / len(team1_votes)
        
        return winner_index, avg_prob
    
    def _generate_signal(self, consensus: float, avg_probability: float) -> str:
        """
        Generate BULLISH/BEARISH/NEUTRAL signal.
        
        Args:
            consensus: Consensus ratio (0-1)
            avg_probability: Average probability (0-1)
            
        Returns:
            Signal string
        """
        # High consensus required for strong signal
        if consensus >= self.consensus_threshold:
            if avg_probability >= self.bullish_threshold:
                return 'BULLISH'
            elif avg_probability < self.bearish_threshold:
                return 'BEARISH'
        
        return 'NEUTRAL'
    
    def _calculate_confidence(self, consensus: float, avg_probability: float) -> float:
        """
        Calculate overall confidence score (0-100).
        
        Args:
            consensus: Model consensus (0-1)
            avg_probability: Average probability (0-1)
            
        Returns:
            Confidence score 0-100
        """
        # Confidence is weighted combination of consensus and probability
        # 60% weight on consensus, 40% on probability
        confidence = (consensus * 0.6 + avg_probability * 0.4) * 100
        return round(confidence, 2)
