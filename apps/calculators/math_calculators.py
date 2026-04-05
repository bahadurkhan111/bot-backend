"""
SportBot - 35 Mathematical Calculators Library
Copiado desde scripts/XGB Accuracy.py para integración Django
"""

import math
import numpy as np
import random
import secrets
from fractions import Fraction
from typing import Union, Tuple, Optional, List


class MathCalculators:
    """Collection of 35 mathematical calculators for feature engineering"""
    
    # ==================== STATISTICAL CALCULATORS ====================
    
    @staticmethod
    def calculate_variance(data: Union[list, np.ndarray], sample: bool = True) -> float:
        """Calculate variance of dataset"""
        try:
            data = np.array(data, dtype=float)
            if len(data) == 0:
                return 0.0
            if sample:
                return float(np.var(data, ddof=1))
            return float(np.var(data, ddof=0))
        except Exception:
            return 0.0
    
    @staticmethod
    def standard_deviation(data: Union[list, np.ndarray], sample: bool = True) -> float:
        """Calculate standard deviation"""
        try:
            data = np.array(data, dtype=float)
            if len(data) == 0:
                return 0.0
            if sample:
                return float(np.std(data, ddof=1))
            return float(np.std(data, ddof=0))
        except Exception:
            return 0.0
    
    @staticmethod
    def mean(data: Union[list, np.ndarray]) -> float:
        """Calculate arithmetic mean"""
        try:
            data = np.array(data, dtype=float)
            if len(data) == 0:
                return 0.0
            return float(np.mean(data))
        except Exception:
            return 0.0
    
    @staticmethod
    def weighted_average(values: Union[list, np.ndarray], 
                        weights: Union[list, np.ndarray]) -> float:
        """Calculate weighted average"""
        try:
            values = np.array(values, dtype=float)
            weights = np.array(weights, dtype=float)
            if len(values) == 0 or len(weights) == 0:
                return 0.0
            return float(np.average(values, weights=weights))
        except Exception:
            return 0.0
    
    # ==================== PERCENTAGE CALCULATORS ====================
    
    @staticmethod
    def percent_error(exact: float, approx: float) -> float:
        """Calculate percentage error"""
        try:
            if exact == 0:
                return 0.0
            return abs(exact - approx) / abs(exact) * 100
        except Exception:
            return 0.0
    
    @staticmethod
    def percentage_increase(initial: float, final: float) -> float:
        """Calculate percentage increase"""
        try:
            if initial == 0:
                return 0.0
            return ((final - initial) / initial) * 100
        except Exception:
            return 0.0
    
    @staticmethod
    def percentage(x: float, y: float) -> float:
        """Calculate x% of y"""
        try:
            return (x / 100) * y
        except Exception:
            return 0.0
    
    @staticmethod
    def percentage_change(old: float, new: float) -> float:
        """Calculate percentage change"""
        try:
            if old == 0:
                return 0.0
            return ((new - old) / old) * 100
        except Exception:
            return 0.0
    
    # ==================== GEOMETRIC CALCULATORS ====================
    
    @staticmethod
    def pythagorean(a: Optional[float] = None, 
                   b: Optional[float] = None, 
                   c: Optional[float] = None) -> float:
        """Solve right triangle using Pythagorean theorem"""
        try:
            if a is not None and b is not None:
                return math.sqrt(a**2 + b**2)
            elif a is not None and c is not None:
                return math.sqrt(abs(c**2 - a**2))
            elif b is not None and c is not None:
                return math.sqrt(abs(c**2 - b**2))
            return 0.0
        except Exception:
            return 0.0
    
    @staticmethod
    def square_root(x: float) -> float:
        """Calculate square root"""
        try:
            if x < 0:
                return 0.0
            return math.sqrt(x)
        except Exception:
            return 0.0
    
    # ==================== LOGARITHMIC CALCULATORS ====================
    
    @staticmethod
    def natural_log(x: float) -> float:
        """Calculate natural logarithm"""
        try:
            if x <= 0:
                return 0.0
            return math.log(x)
        except Exception:
            return 0.0
    
    @staticmethod
    def logarithm(x: float, base: float = 10) -> float:
        """Calculate logarithm with any base"""
        try:
            if x <= 0 or base <= 0 or base == 1:
                return 0.0
            return math.log(x, base)
        except Exception:
            return 0.0
    
    @staticmethod
    def antilog(y: float, base: float = 10) -> float:
        """Calculate antilog"""
        try:
            if base == math.e:
                return math.exp(y)
            return base ** y
        except Exception:
            return 0.0
    
    # ==================== TRIGONOMETRIC CALCULATORS ====================
    
    @staticmethod
    def sine(angle: float, degrees: bool = True) -> float:
        """Calculate sine of angle"""
        try:
            if degrees:
                angle = math.radians(angle)
            return math.sin(angle)
        except Exception:
            return 0.0
    
    @staticmethod
    def cosine(angle: float, degrees: bool = True) -> float:
        """Calculate cosine of angle"""
        try:
            if degrees:
                angle = math.radians(angle)
            return math.cos(angle)
        except Exception:
            return 0.0
    
    @staticmethod
    def tangent(angle: float, degrees: bool = True) -> float:
        """Calculate tangent of angle"""
        try:
            if degrees:
                angle = math.radians(angle)
            return math.tan(angle)
        except Exception:
            return 0.0
    
    @staticmethod
    def arcsine(x: float, degrees: bool = True) -> float:
        """Calculate inverse sine"""
        try:
            if x < -1 or x > 1:
                return 0.0
            result = math.asin(x)
            return math.degrees(result) if degrees else result
        except Exception:
            return 0.0
    
    @staticmethod
    def arccosine(x: float, degrees: bool = True) -> float:
        """Calculate inverse cosine"""
        try:
            if x < -1 or x > 1:
                return 0.0
            result = math.acos(x)
            return math.degrees(result) if degrees else result
        except Exception:
            return 0.0
    
    @staticmethod
    def arctangent(x: float, degrees: bool = True) -> float:
        """Calculate inverse tangent"""
        try:
            result = math.atan(x)
            return math.degrees(result) if degrees else result
        except Exception:
            return 0.0
    
    # ==================== ALGEBRAIC CALCULATORS ====================
    
    @staticmethod
    def factorial(n: float) -> float:
        """Calculate factorial"""
        try:
            if n < 0:
                return 0.0
            return float(math.factorial(int(n)))
        except Exception:
            return 0.0
    
    @staticmethod
    def exponent(base: float, power: float) -> float:
        """Calculate base^power"""
        try:
            return base ** power
        except Exception:
            return 0.0
    
    @staticmethod
    def quadratic_solver(a: float, b: float, c: float) -> Tuple[Optional[float], Optional[float]]:
        """Solve ax² + bx + c = 0"""
        try:
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return (0.0, 0.0)
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return (x1, x2)
        except Exception:
            return (0.0, 0.0)
    
    # ==================== FRACTION CALCULATORS ====================
    
    @staticmethod
    def add_fractions(a: float, b: float, c: float, d: float) -> float:
        """Add fractions: a/b + c/d"""
        try:
            result = Fraction(int(a), int(b)) + Fraction(int(c), int(d))
            return float(result)
        except Exception:
            return 0.0
    
    @staticmethod
    def subtract_fractions(a: float, b: float, c: float, d: float) -> float:
        """Subtract fractions: a/b - c/d"""
        try:
            result = Fraction(int(a), int(b)) - Fraction(int(c), int(d))
            return float(result)
        except Exception:
            return 0.0
    
    @staticmethod
    def multiply_fractions(a: float, b: float, c: float, d: float) -> float:
        """Multiply fractions: (a/b) × (c/d)"""
        try:
            result = Fraction(int(a), int(b)) * Fraction(int(c), int(d))
            return float(result)
        except Exception:
            return 0.0
    
    @staticmethod
    def divide_fractions(a: float, b: float, c: float, d: float) -> float:
        """Divide fractions: (a/b) ÷ (c/d)"""
        try:
            result = Fraction(int(a), int(b)) / Fraction(int(c), int(d))
            return float(result)
        except Exception:
            return 0.0
    
    # ==================== NUMBER THEORY CALCULATORS ====================
    
    @staticmethod
    def gcd(a: float, b: float) -> float:
        """Calculate GCD using Euclidean algorithm"""
        try:
            return float(math.gcd(int(abs(a)), int(abs(b))))
        except Exception:
            return 1.0
    
    @staticmethod
    def lcm(a: float, b: float) -> float:
        """Calculate LCM"""
        try:
            a_int = int(abs(a))
            b_int = int(abs(b))
            return float(abs(a_int * b_int) // math.gcd(a_int, b_int))
        except Exception:
            return 0.0
    
    @staticmethod
    def simplify_ratio(a: float, b: float) -> Tuple[float, float]:
        """Simplify ratio a:b"""
        try:
            gcd_val = math.gcd(int(abs(a)), int(abs(b)))
            return (float(int(a) // gcd_val), float(int(b) // gcd_val))
        except Exception:
            return (0.0, 0.0)
    
    # ==================== GROWTH CALCULATORS ====================
    
    @staticmethod
    def exponential_growth(x0: float, rate: float, time: float) -> float:
        """Calculate exponential growth"""
        try:
            return x0 * (1 + rate) ** time
        except Exception:
            return 0.0
    
    # ==================== RANDOM NUMBER GENERATOR ====================
    
    @staticmethod
    def generate_random(min_val: float, max_val: float, secure: bool = False) -> float:
        """Generate random number in range"""
        try:
            if secure:
                return secrets.SystemRandom().uniform(min_val, max_val)
            return random.uniform(min_val, max_val)
        except Exception:
            return 0.0
    
    # ==================== BASIC ARITHMETIC CALCULATORS ====================
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Basic addition"""
        try:
            return a + b
        except Exception:
            return 0.0
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Basic subtraction"""
        try:
            return a - b
        except Exception:
            return 0.0
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Basic multiplication"""
        try:
            return a * b
        except Exception:
            return 0.0
    
    @staticmethod
    def divide(a: float, b: float) -> Tuple[float, float]:
        """Basic division with remainder"""
        try:
            if b == 0:
                return (0.0, 0.0)
            quotient = float(a // b)
            remainder = float(a % b)
            return (quotient, remainder)
        except Exception:
            return (0.0, 0.0)


# Helper function to apply all 35 calculators to a single value
def apply_all_calculators_to_value(value: float) -> dict:
    """
    Apply all 35 mathematical calculators to a single prediction value.
    Returns a dictionary with calculator names and results.
    """
    calc = MathCalculators()
    
    results = {
        # Logarithmic (3)
        'natural_log': calc.natural_log(abs(value) + 1),
        'log10': calc.logarithm(abs(value) + 1, 10),
        'log2': calc.logarithm(abs(value) + 1, 2),
        
        # Geometric (2)
        'square_root': calc.square_root(abs(value)),
        'pythagorean_with_3': calc.pythagorean(abs(value), 3),
        
        # Exponential (4)
        'squared': calc.exponent(value, 2),
        'cubed': calc.exponent(value, 3),
        'power_1_5': calc.exponent(abs(value), 1.5),
        'cube_root': calc.exponent(abs(value), 1/3),
        
        # Trigonometric (6)
        'sine': calc.sine(value % 360),
        'cosine': calc.cosine(value % 360),
        'tangent': calc.tangent(value % 360),
        'arcsine': calc.arcsine((value % 2) / 2) if abs((value % 2) / 2) <= 1 else 0,
        'arccosine': calc.arccosine((value % 2) / 2) if abs((value % 2) / 2) <= 1 else 0,
        'arctangent': calc.arctangent(value / 100),
        
        # Algebraic (2)
        'factorial': calc.factorial(min(abs(int(value)), 10)),
        'exponential': calc.antilog(value / 100, math.e),
        
        # Basic arithmetic (6)
        'absolute': abs(value),
        'reciprocal': 1 / (value + 1e-10),
        'add_100': calc.add(value, 100),
        'subtract_from_1000': calc.subtract(1000, value),
        'multiply_by_2': calc.multiply(value, 2),
        'divide_by_2': calc.divide(value, 2)[0],
        
        # Rounding (4)
        'floor': math.floor(value),
        'ceiling': math.ceil(value),
        'round': round(value),
        'modulo_10': value % 10,
        
        # Percentage (4)
        'percentage_of_100': calc.percentage(value, 100),
        'pct_increase_from_100': calc.percentage_increase(100, value),
        'pct_change_to_500': calc.percentage_change(value, 500),
        'pct_error_vs_500': calc.percent_error(500, value),
        
        # Number theory (2)
        'gcd_with_100': calc.gcd(abs(value), 100),
        'lcm_with_10': calc.lcm(abs(value), 10),
        
        # Growth (1)
        'exp_growth_5pct': calc.exponential_growth(value, 0.05, 1),
        
        # Antilog (1)
        'antilog_base10': calc.antilog(value / 100, 10),
    }
    
    return results
