"""
ML model loader service.
Loads pre-trained .pkl models and provides prediction interface.
"""
import pickle
import logging
from pathlib import Path
from typing import Dict, Any, Optional
import numpy as np
from django.conf import settings

logger = logging.getLogger(__name__)


class ModelLoader:
    """
    Service for loading and managing ML models.
    Implements singleton pattern to load models only once.
    """
    
    _instance: Optional['ModelLoader'] = None
    _models: Dict[str, Any] = {}
    
    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize model loader."""
        if self._initialized:
            return
        
        self._initialized = True
        self.model_files = settings.ML_MODEL_FILES
        self._models = {}
        self._load_all_models()
    
    def _load_all_models(self) -> None:
        """Load all ML models from disk."""
        for model_name, model_path in self.model_files.items():
            try:
                self._load_model(model_name, model_path)
            except Exception as e:
                logger.error(f"Failed to load model {model_name} from {model_path}: {e}")
    
    def _load_model(self, model_name: str, model_path: Path) -> None:
        """
        Load a single model from disk.
        
        Args:
            model_name: Name identifier for the model
            model_path: Path to the .pkl file
        """
        if not model_path.exists():
            logger.warning(f"Model file not found: {model_path}")
            return
        
        try:
            with open(model_path, 'rb') as f:
                model = pickle.load(f)
            self._models[model_name] = model
            logger.info(f"Successfully loaded model: {model_name}")
        except Exception as e:
            logger.error(f"Error loading model {model_name}: {e}")
            raise
    
    def get_model(self, model_name: str) -> Optional[Any]:
        """
        Get a loaded model by name.
        
        Args:
            model_name: Name of the model
            
        Returns:
            Model object or None if not loaded
        """
        return self._models.get(model_name)
    
    def is_model_loaded(self, model_name: str) -> bool:
        """
        Check if a model is loaded.
        
        Args:
            model_name: Name of the model
            
        Returns:
            True if model is loaded, False otherwise
        """
        return model_name in self._models
    
    def get_loaded_models(self) -> list:
        """
        Get list of all loaded model names.
        
        Returns:
            List of model names
        """
        return list(self._models.keys())
    
    def predict(self, model_name: str, features: np.ndarray) -> Optional[np.ndarray]:
        """
        Make prediction using a specific model.
        
        Args:
            model_name: Name of the model to use
            features: Feature vector as numpy array
            
        Returns:
            Prediction array or None if model not available
        """
        model = self.get_model(model_name)
        if model is None:
            logger.error(f"Model {model_name} not available for prediction")
            return None
        
        try:
            # Ensure features are 2D array
            if features.ndim == 1:
                features = features.reshape(1, -1)
            
            # Make prediction - use predict() for regression models
            prediction = model.predict(features)
            logger.debug(f"Prediction from {model_name}: {prediction}")
            return prediction
        except Exception as e:
            logger.error(f"Error making prediction with {model_name}: {e}")
            return None
    
    def reload_model(self, model_name: str) -> bool:
        """
        Reload a specific model from disk.
        
        Args:
            model_name: Name of the model to reload
            
        Returns:
            True if successful, False otherwise
        """
        if model_name not in self.model_files:
            logger.error(f"Unknown model name: {model_name}")
            return False
        
        try:
            self._load_model(model_name, self.model_files[model_name])
            logger.info(f"Reloaded model: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Failed to reload model {model_name}: {e}")
            return False
    
    def get_model_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Get information about all loaded models.
        
        Returns:
            Dictionary with model information
        """
        info = {}
        for model_name, model in self._models.items():
            info[model_name] = {
                'loaded': True,
                'type': type(model).__name__,
                'file': str(self.model_files.get(model_name, 'Unknown')),
            }
        
        # Add info about models that failed to load
        for model_name in self.model_files:
            if model_name not in self._models:
                info[model_name] = {
                    'loaded': False,
                    'file': str(self.model_files[model_name]),
                }
        
        return info


# Global instance
model_loader = ModelLoader()
