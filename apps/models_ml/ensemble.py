"""
Ensemble prediction system combining 4 ML models.
"""
import logging
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional
from django.conf import settings
from .loader import model_loader
from .signal_generator import SignalGenerator, EnsembleResult
from .prediction_analyzer import prediction_analyzer

logger = logging.getLogger(__name__)

# The 14 gematria feature names expected by the trained models
FEATURE_COLUMNS = [
    'ordinal', 'reverse_ordinal', 'reduction', 'reverse_reduction',
    'standard', 'reverse_standard', 'latin', 'jewish',
    'english_extended', 'francis_bacon', 'satanic', 'septenary',
    'chaldean', 'keypad'
]


def create_feature_dataframe(gematria_values: Dict[str, int]) -> pd.DataFrame:
    """
    Create a DataFrame with 14 features from gematria values.
    Maps gematria calculator outputs to the feature columns the ML models expect.

    Args:
        gematria_values: Dict of calculator_name -> value

    Returns:
        DataFrame with one row and 14 feature columns
    """
    features = {}
    for col in FEATURE_COLUMNS:
        features[col] = gematria_values.get(col, 0)
    return pd.DataFrame([features])


class EnsemblePredictor:
    """
    Ensemble system that combines predictions from 4 ML models.
    """

    MODEL_NAMES = ['lasso', 'xgboost', 'linear', 'model4']

    def __init__(self):
        """Initialize ensemble predictor."""
        self.model_loader = model_loader
        self.signal_generator = SignalGenerator()
        self._validate_models()

    def _validate_models(self) -> None:
        """Validate that all required models are loaded."""
        loaded_models = self.model_loader.get_loaded_models()
        missing_models = [m for m in self.MODEL_NAMES if m not in loaded_models]

        if missing_models:
            logger.warning(f"Missing models: {missing_models}")
        else:
            logger.info("All ensemble models loaded successfully")

    def create_feature_vector(
        self,
        team1_gematria: Dict[str, int],
        team2_gematria: Dict[str, int]
    ) -> np.ndarray:
        """
        Create feature vector from gematria values.

        Uses only team1 gematria values mapped to 14 features expected by models.
        Models were trained to predict Sumerian value from other gematria values.

        Args:
            team1_gematria: Gematria values for team1
            team2_gematria: Gematria values for team2 (not used in current model)

        Returns:
            Feature vector as numpy array (14 features)
        """
        df = create_feature_dataframe(team1_gematria)
        return df.values[0]  # Return as 1D array
    
    def predict(
        self,
        features: np.ndarray,
        team1_name: str,
        team2_name: str
    ) -> Optional[Tuple[EnsembleResult, Dict[str, float]]]:
        """
        Make ensemble prediction using all models.
        
        Models predict Sumerian value. Higher value = stronger prediction.
        
        Args:
            features: Feature vector (14 features)
            team1_name: Name of team1
            team2_name: Name of team2
            
        Returns:
            Tuple of (EnsembleResult, raw_predictions) or None if prediction fails
        """
        # Collect predictions from all models
        raw_predictions = {}
        
        # Reshape features for sklearn models (expects 2D array)
        features_2d = features.reshape(1, -1)
        
        for model_name in self.MODEL_NAMES:
            try:
                prediction = self.model_loader.predict(model_name, features_2d)
                if prediction is not None:
                    # Models output regression value (predicted Sumerian)
                    predicted_value = float(prediction[0])
                    raw_predictions[model_name] = predicted_value
                    logger.debug(f"{model_name} prediction: {predicted_value:.2f}")
                else:
                    logger.warning(f"Model {model_name} returned None")
            except Exception as e:
                logger.error(f"Error getting prediction from {model_name}: {e}")
        
        if not raw_predictions:
            logger.error("No models produced valid predictions")
            return None
        
        # Generate ensemble signal
        ensemble_result = self.signal_generator.generate_signal(
            raw_predictions,
            team1_name,
            team2_name
        )
        
        return ensemble_result, raw_predictions
    
    def predict_game(
        self,
        team1_gematria: Dict[str, int],
        team2_gematria: Dict[str, int],
        team1_name: str,
        team2_name: str
    ) -> Optional[Dict]:
        """
        Make complete game prediction from gematria values.
        Includes ensemble prediction + 35 mathematical calculator analysis.
        
        Args:
            team1_gematria: Gematria values for team1
            team2_gematria: Gematria values for team2
            team1_name: Name of team1
            team2_name: Name of team2
            
        Returns:
            Complete prediction dict with ensemble result, raw predictions, 
            features, and mathematical analysis, or None if prediction fails
        """
        try:
            # Create feature vector
            features = self.create_feature_vector(team1_gematria, team2_gematria)
            logger.info(f"Created feature vector with {len(features)} features")
            
            # Make prediction
            result = self.predict(features, team1_name, team2_name)
            
            if result is None:
                return None
            
            ensemble_result, raw_predictions = result
            
            # Apply 35 mathematical calculators to results
            analysis_summary = prediction_analyzer.create_analysis_summary(raw_predictions)
            
            # Build complete response
            return {
                'ensemble_result': ensemble_result,
                'raw_predictions': raw_predictions,
                'features': features.tolist(),
                'analysis': analysis_summary,
                'team1_name': team1_name,
                'team2_name': team2_name
            }
            
        except Exception as e:
            logger.error(f"Error in predict_game: {e}")
            return None
    
    def get_model_status(self) -> Dict[str, bool]:
        """
        Get status of all ensemble models.
        
        Returns:
            Dictionary mapping model names to loaded status
        """
        return {
            model_name: self.model_loader.is_model_loaded(model_name)
            for model_name in self.MODEL_NAMES
        }


# Global instance
ensemble_predictor = EnsemblePredictor()
