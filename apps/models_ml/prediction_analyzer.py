"""
Post-processing: Apply 35 mathematical calculators to prediction results.
Analyzes the ensemble prediction using advanced mathematical transformations.
"""
from typing import Dict
from apps.calculators.math_calculators import MathCalculators, apply_all_calculators_to_value


class PredictionAnalyzer:
    """
    Applies 35 mathematical calculators to analyze prediction results.
    """
    
    def __init__(self):
        """Initialize analyzer with math calculators."""
        self.calc = MathCalculators()
    
    def analyze_prediction(self, prediction_value: float) -> Dict[str, float]:
        """
        Apply all 35 mathematical calculators to a prediction value.
        
        This provides deep mathematical analysis of the prediction including:
        - Logarithmic transformations (ln, log10, log2)
        - Trigonometric analysis (sin, cos, tan, arcsin, arccos, arctan)
        - Exponential operations (squares, cubes, roots, etc.)
        - Statistical measures (variance, std, mean, etc.)
        - Number theory (GCD, LCM, factorials)
        - Growth calculations (exponential growth)
        
        Args:
            prediction_value: The predicted value from ensemble
            
        Returns:
            Dictionary with 35 calculator results
        """
        return apply_all_calculators_to_value(prediction_value)
    
    def analyze_ensemble(self, raw_predictions: Dict[str, float]) -> Dict[str, Dict[str, float]]:
        """
        Apply 35 calculators to each model's prediction.
        
        Args:
            raw_predictions: Dict of {model_name: prediction_value}
            
        Returns:
            Dict of {model_name: {calculator_name: result}}
        """
        results = {}
        
        for model_name, prediction in raw_predictions.items():
            results[model_name] = self.analyze_prediction(prediction)
        
        return results
    
    def get_average_prediction(self, raw_predictions: Dict[str, float]) -> float:
        """
        Calculate average prediction across all models.
        
        Args:
            raw_predictions: Dict of {model_name: prediction_value}
            
        Returns:
            Average prediction value
        """
        if not raw_predictions:
            return 0.0
        
        return sum(raw_predictions.values()) / len(raw_predictions)
    
    def get_weighted_prediction(
        self, 
        raw_predictions: Dict[str, float],
        weights: Dict[str, float] = None
    ) -> float:
        """
        Calculate weighted prediction across all models.
        
        Args:
            raw_predictions: Dict of {model_name: prediction_value}
            weights: Optional dict of {model_name: weight}. Defaults to equal weights.
            
        Returns:
            Weighted prediction value
        """
        if not raw_predictions:
            return 0.0
        
        # Default to equal weights
        if weights is None:
            weights = {name: 1.0 for name in raw_predictions.keys()}
        
        # Normalize weights to sum to 1
        total_weight = sum(weights.values())
        if total_weight == 0:
            return self.get_average_prediction(raw_predictions)
        
        normalized_weights = {k: v / total_weight for k, v in weights.items()}
        
        # Calculate weighted sum
        weighted_sum = sum(
            raw_predictions[name] * normalized_weights.get(name, 0)
            for name in raw_predictions.keys()
        )
        
        return weighted_sum
    
    def create_analysis_summary(
        self,
        raw_predictions: Dict[str, float]
    ) -> Dict[str, any]:
        """
        Create comprehensive analysis summary with key metrics.
        
        Args:
            raw_predictions: Dict of {model_name: prediction_value}
            
        Returns:
            Summary dict with average, weighted, and calculator results
        """
        avg_prediction = self.get_average_prediction(raw_predictions)
        
        # Apply 35 calculators to average prediction
        calculator_results = self.analyze_prediction(avg_prediction)
        
        # Get prediction stats
        predictions_list = list(raw_predictions.values())
        
        summary = {
            'average_prediction': avg_prediction,
            'min_prediction': min(predictions_list) if predictions_list else 0,
            'max_prediction': max(predictions_list) if predictions_list else 0,
            'variance': self.calc.calculate_variance(predictions_list) if len(predictions_list) > 1 else 0,
            'std_deviation': self.calc.standard_deviation(predictions_list) if len(predictions_list) > 1 else 0,
            'calculator_results': calculator_results,
            'individual_predictions': raw_predictions
        }
        
        return summary


# Global instance
prediction_analyzer = PredictionAnalyzer()
