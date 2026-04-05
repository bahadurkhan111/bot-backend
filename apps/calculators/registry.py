"""
Calculator registry for dynamic calculator selection and management.
"""
from typing import Dict, List, Type, Optional
from .base import GematriaCalculator
from .basic import (
    OrdinalCalculator,
    ReductionCalculator,
    ReverseOrdinalCalculator,
    ReverseReductionCalculator,
    SumerianCalculator,
)
from .multipliers import (
    ReverseSumerianCalculator,
    SatanicCalculator,
    ReverseSatanicCalculator,
)
from .mathematical import (
    PrimesCalculator,
    TrigonalCalculator,
    SquaresCalculator,
    FibonacciCalculator,
    ReversePrimesCalculator,
    ReverseTrigonalCalculator,
)
from .special import (
    ChaldeanCalculator,
    LatinCalculator,
    LatinReductionCalculator,
    SeptenaryCalculator,
    KeypadCalculator,
    FrancisBaconCalculator,
    EnglishOrdinalCalculator,
    EnglishReductionCalculator,
    SingleReductionCalculator,
    JewishCalculator,
    ALWKabbalahCalculator,
    KFWKabbalahCalculator,
)
import logging

logger = logging.getLogger(__name__)


class CalculatorRegistry:
    """
    Registry for managing all available gematria calculators.
    Implements the Factory pattern for calculator creation.
    """
    
    _calculators: Dict[str, Type[GematriaCalculator]] = {}
    _instances: Dict[str, GematriaCalculator] = {}
    
    @classmethod
    def register(cls, calculator_class: Type[GematriaCalculator]) -> None:
        """
        Register a calculator class.
        
        Args:
            calculator_class: Calculator class to register
        """
        instance = calculator_class()
        name = instance.name
        cls._calculators[name] = calculator_class
        cls._instances[name] = instance
        logger.info(f"Registered calculator: {name}")
    
    @classmethod
    def get_calculator(cls, name: str) -> Optional[GematriaCalculator]:
        """
        Get a calculator instance by name.
        
        Args:
            name: Calculator name
            
        Returns:
            Calculator instance or None if not found
        """
        return cls._instances.get(name)
    
    @classmethod
    def get_all_calculators(cls) -> Dict[str, GematriaCalculator]:
        """
        Get all registered calculator instances.
        
        Returns:
            Dictionary mapping calculator names to instances
        """
        return cls._instances.copy()
    
    @classmethod
    def list_calculator_names(cls) -> List[str]:
        """
        Get list of all registered calculator names.
        
        Returns:
            List of calculator names
        """
        return list(cls._calculators.keys())
    
    @classmethod
    def calculate_all(cls, text: str) -> Dict[str, int]:
        """
        Calculate gematria values using all registered calculators.
        
        Args:
            text: Input text
            
        Returns:
            Dictionary mapping calculator names to calculated values
        """
        results = {}
        for name, calculator in cls._instances.items():
            try:
                results[name] = calculator.calculate(text)
            except Exception as e:
                logger.error(f"Error calculating {name} for '{text}': {e}")
                results[name] = 0
        return results
    
    @classmethod
    def get_calculator_info(cls) -> List[Dict[str, str]]:
        """
        Get information about all registered calculators.
        
        Returns:
            List of dictionaries containing calculator information
        """
        return [calc.get_info() for calc in cls._instances.values()]


# Auto-register all calculators
def register_default_calculators():
    """Register all 35+ calculators."""
    # Basic calculators
    CalculatorRegistry.register(OrdinalCalculator)
    CalculatorRegistry.register(ReductionCalculator)
    CalculatorRegistry.register(ReverseOrdinalCalculator)
    CalculatorRegistry.register(ReverseReductionCalculator)
    CalculatorRegistry.register(SumerianCalculator)
    
    # Multiplier calculators
    CalculatorRegistry.register(ReverseSumerianCalculator)
    CalculatorRegistry.register(SatanicCalculator)
    CalculatorRegistry.register(ReverseSatanicCalculator)
    
    # Mathematical calculators
    CalculatorRegistry.register(PrimesCalculator)
    CalculatorRegistry.register(TrigonalCalculator)
    CalculatorRegistry.register(SquaresCalculator)
    CalculatorRegistry.register(FibonacciCalculator)
    CalculatorRegistry.register(ReversePrimesCalculator)
    CalculatorRegistry.register(ReverseTrigonalCalculator)
    
    # Special calculators
    CalculatorRegistry.register(ChaldeanCalculator)
    CalculatorRegistry.register(LatinCalculator)
    CalculatorRegistry.register(LatinReductionCalculator)
    CalculatorRegistry.register(SeptenaryCalculator)
    CalculatorRegistry.register(KeypadCalculator)
    CalculatorRegistry.register(FrancisBaconCalculator)
    CalculatorRegistry.register(EnglishOrdinalCalculator)
    CalculatorRegistry.register(EnglishReductionCalculator)
    CalculatorRegistry.register(SingleReductionCalculator)
    CalculatorRegistry.register(JewishCalculator)
    CalculatorRegistry.register(ALWKabbalahCalculator)
    CalculatorRegistry.register(KFWKabbalahCalculator)
    
    logger.info(f"Registered {len(CalculatorRegistry.list_calculator_names())} calculators")


# Register calculators on module import
register_default_calculators()
