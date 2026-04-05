"""
Mathematical Calculators Library for Sports Prediction ML Models
Contains 35 calculator functions from RapidTables.com
Integrated with error handling and comprehensive docstrings
"""

import numpy as np
import math
import random
import secrets
from fractions import Fraction
from typing import Union, Tuple, Optional, List


class MathCalculators:
    """Collection of 35 mathematical calculators for feature engineering"""
    
    # ==================== STATISTICAL CALCULATORS ====================
    
    @staticmethod
    def calculate_variance(data: Union[list, np.ndarray], sample: bool = True) -> float:
        """
        Calculate variance of dataset
        Population: σ² = Σ(x - μ)² / n
        Sample: s² = Σ(x - x̄)² / (n-1)
        
        Args:
            data: Array-like data
            sample: If True, calculate sample variance; else population variance
            
        Returns:
            Variance value
        """
        try:
            data = np.array(data, dtype=float)
            if len(data) == 0:
                return 0.0
            if sample:
                return float(np.var(data, ddof=1))  # Sample variance
            return float(np.var(data, ddof=0))      # Population variance
        except Exception as e:
            return 0.0
    
    @staticmethod
    def standard_deviation(data: Union[list, np.ndarray], sample: bool = True) -> float:
        """
        Calculate standard deviation
        Population: σ = √[Σ(x - μ)² / n]
        Sample: s = √[Σ(x - x̄)² / (n-1)]
        
        Args:
            data: Array-like data
            sample: If True, calculate sample std; else population std
            
        Returns:
            Standard deviation value
        """
        try:
            data = np.array(data, dtype=float)
            if len(data) == 0:
                return 0.0
            if sample:
                return float(np.std(data, ddof=1))
            return float(np.std(data, ddof=0))
        except Exception as e:
            return 0.0
    
    @staticmethod
    def mean(data: Union[list, np.ndarray]) -> float:
        """
        Calculate arithmetic mean: μ = (Σx) / n
        
        Args:
            data: Array-like data
            
        Returns:
            Mean value
        """
        try:
            data = np.array(data, dtype=float)
            if len(data) == 0:
                return 0.0
            return float(np.mean(data))
        except Exception as e:
            return 0.0
    
    @staticmethod
    def weighted_average(values: Union[list, np.ndarray], 
                        weights: Union[list, np.ndarray]) -> float:
        """
        Calculate weighted average: Σ(w_i × x_i) / Σw_i
        
        Args:
            values: Array of values
            weights: Array of weights
            
        Returns:
            Weighted average
        """
        try:
            values = np.array(values, dtype=float)
            weights = np.array(weights, dtype=float)
            if len(values) == 0 or len(weights) == 0:
                return 0.0
            return float(np.average(values, weights=weights))
        except Exception as e:
            return 0.0
    
    # ==================== PERCENTAGE CALCULATORS ====================
    
    @staticmethod
    def percent_error(exact: float, approx: float) -> float:
        """
        Calculate percentage error
        Formula: δ = 100% × |V_exact - V_approx| / |V_exact|
        
        Args:
            exact: Exact value
            approx: Approximate value
            
        Returns:
            Percentage error
        """
        try:
            if exact == 0:
                return 0.0
            return abs(exact - approx) / abs(exact) * 100
        except Exception as e:
            return 0.0
    
    @staticmethod
    def percentage_increase(initial: float, final: float) -> float:
        """
        Calculate percentage increase
        Formula: (V_final - V_initial) / V_initial × 100%
        
        Args:
            initial: Initial value
            final: Final value
            
        Returns:
            Percentage increase (negative if decrease)
        """
        try:
            if initial == 0:
                return 0.0
            return ((final - initial) / initial) * 100
        except Exception as e:
            return 0.0
    
    @staticmethod
    def percentage(x: float, y: float) -> float:
        """
        Calculate x% of y: (x/100) × y
        
        Args:
            x: Percentage value
            y: Base value
            
        Returns:
            Result of x% of y
        """
        try:
            return (x / 100) * y
        except Exception as e:
            return 0.0
    
    @staticmethod
    def percentage_change(old: float, new: float) -> float:
        """
        Calculate percentage change: (new - old) / old × 100%
        
        Args:
            old: Old value
            new: New value
            
        Returns:
            Percentage change
        """
        try:
            if old == 0:
                return 0.0
            return ((new - old) / old) * 100
        except Exception as e:
            return 0.0
    
    # ==================== GEOMETRIC CALCULATORS ====================
    
    @staticmethod
    def pythagorean(a: Optional[float] = None, 
                   b: Optional[float] = None, 
                   c: Optional[float] = None) -> float:
        """
        Solve right triangle using Pythagorean theorem
        c² = a² + b²
        
        Args:
            a: Side a
            b: Side b
            c: Hypotenuse c
            
        Returns:
            Missing side length
        """
        try:
            if a is not None and b is not None:
                return math.sqrt(a**2 + b**2)
            elif a is not None and c is not None:
                return math.sqrt(abs(c**2 - a**2))
            elif b is not None and c is not None:
                return math.sqrt(abs(c**2 - b**2))
            return 0.0
        except Exception as e:
            return 0.0
    
    @staticmethod
    def square_root(x: float) -> float:
        """
        Calculate square root: √x
        
        Args:
            x: Value
            
        Returns:
            Square root of x
        """
        try:
            if x < 0:
                return 0.0
            return math.sqrt(x)
        except Exception as e:
            return 0.0
    
    # ==================== LOGARITHMIC CALCULATORS ====================
    
    @staticmethod
    def natural_log(x: float) -> float:
        """
        Calculate natural logarithm: ln(x) = log_e(x)
        
        Args:
            x: Value (must be positive)
            
        Returns:
            Natural logarithm
        """
        try:
            if x <= 0:
                return 0.0
            return math.log(x)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def logarithm(x: float, base: float = 10) -> float:
        """
        Calculate logarithm with any base
        Formula: log_b(x) = log_c(x) / log_c(b)
        
        Args:
            x: Value
            base: Base of logarithm
            
        Returns:
            Logarithm value
        """
        try:
            if x <= 0 or base <= 0 or base == 1:
                return 0.0
            return math.log(x, base)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def antilog(y: float, base: float = 10) -> float:
        """
        Calculate antilog: antilog_b(y) = b^y
        
        Args:
            y: Exponent
            base: Base
            
        Returns:
            Antilog value
        """
        try:
            if base == math.e:
                return math.exp(y)
            return base ** y
        except Exception as e:
            return 0.0
    
    # ==================== TRIGONOMETRIC CALCULATORS ====================
    
    @staticmethod
    def sine(angle: float, degrees: bool = True) -> float:
        """
        Calculate sine of angle
        
        Args:
            angle: Angle value
            degrees: If True, angle is in degrees; else radians
            
        Returns:
            Sine value
        """
        try:
            if degrees:
                angle = math.radians(angle)
            return math.sin(angle)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def cosine(angle: float, degrees: bool = True) -> float:
        """
        Calculate cosine of angle
        
        Args:
            angle: Angle value
            degrees: If True, angle is in degrees; else radians
            
        Returns:
            Cosine value
        """
        try:
            if degrees:
                angle = math.radians(angle)
            return math.cos(angle)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def tangent(angle: float, degrees: bool = True) -> float:
        """
        Calculate tangent of angle
        
        Args:
            angle: Angle value
            degrees: If True, angle is in degrees; else radians
            
        Returns:
            Tangent value
        """
        try:
            if degrees:
                angle = math.radians(angle)
            return math.tan(angle)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def arcsine(x: float, degrees: bool = True) -> float:
        """
        Calculate inverse sine: arcsin(x)
        Domain: [-1, 1]
        
        Args:
            x: Value
            degrees: If True, return in degrees; else radians
            
        Returns:
            Arcsine value
        """
        try:
            if x < -1 or x > 1:
                return 0.0
            result = math.asin(x)
            return math.degrees(result) if degrees else result
        except Exception as e:
            return 0.0
    
    @staticmethod
    def arccosine(x: float, degrees: bool = True) -> float:
        """
        Calculate inverse cosine: arccos(x)
        Domain: [-1, 1]
        
        Args:
            x: Value
            degrees: If True, return in degrees; else radians
            
        Returns:
            Arccosine value
        """
        try:
            if x < -1 or x > 1:
                return 0.0
            result = math.acos(x)
            return math.degrees(result) if degrees else result
        except Exception as e:
            return 0.0
    
    @staticmethod
    def arctangent(x: float, degrees: bool = True) -> float:
        """
        Calculate inverse tangent: arctan(x)
        
        Args:
            x: Value
            degrees: If True, return in degrees; else radians
            
        Returns:
            Arctangent value
        """
        try:
            result = math.atan(x)
            return math.degrees(result) if degrees else result
        except Exception as e:
            return 0.0
    
    # ==================== ALGEBRAIC CALCULATORS ====================
    
    @staticmethod
    def factorial(n: float) -> float:
        """
        Calculate factorial: n! = 1 × 2 × 3 × ... × n
        
        Args:
            n: Non-negative integer
            
        Returns:
            Factorial value
        """
        try:
            if n < 0:
                return 0.0
            return float(math.factorial(int(n)))
        except Exception as e:
            return 0.0
    
    @staticmethod
    def exponent(base: float, power: float) -> float:
        """
        Calculate base^power
        
        Args:
            base: Base value
            power: Exponent
            
        Returns:
            Result of base^power
        """
        try:
            return base ** power
        except Exception as e:
            return 0.0
    
    @staticmethod
    def quadratic_solver(a: float, b: float, c: float) -> Tuple[Optional[float], Optional[float]]:
        """
        Solve ax² + bx + c = 0
        Formula: x = [-b ± √(b² - 4ac)] / 2a
        
        Args:
            a: Coefficient of x²
            b: Coefficient of x
            c: Constant term
            
        Returns:
            Tuple of two solutions (or None if no real solutions)
        """
        try:
            discriminant = b**2 - 4*a*c
            if discriminant < 0:
                return (0.0, 0.0)  # No real solutions
            x1 = (-b + math.sqrt(discriminant)) / (2*a)
            x2 = (-b - math.sqrt(discriminant)) / (2*a)
            return (x1, x2)
        except Exception as e:
            return (0.0, 0.0)
    
    # ==================== FRACTION CALCULATORS ====================
    
    @staticmethod
    def add_fractions(a: float, b: float, c: float, d: float) -> float:
        """
        Add fractions: a/b + c/d = (ad + bc) / bd
        
        Args:
            a, b: First fraction (a/b)
            c, d: Second fraction (c/d)
            
        Returns:
            Result as decimal
        """
        try:
            result = Fraction(int(a), int(b)) + Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def subtract_fractions(a: float, b: float, c: float, d: float) -> float:
        """
        Subtract fractions: a/b - c/d = (ad - bc) / bd
        
        Args:
            a, b: First fraction (a/b)
            c, d: Second fraction (c/d)
            
        Returns:
            Result as decimal
        """
        try:
            result = Fraction(int(a), int(b)) - Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def multiply_fractions(a: float, b: float, c: float, d: float) -> float:
        """
        Multiply fractions: (a/b) × (c/d) = (ac) / (bd)
        
        Args:
            a, b: First fraction (a/b)
            c, d: Second fraction (c/d)
            
        Returns:
            Result as decimal
        """
        try:
            result = Fraction(int(a), int(b)) * Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def divide_fractions(a: float, b: float, c: float, d: float) -> float:
        """
        Divide fractions: (a/b) ÷ (c/d) = (ad) / (bc)
        
        Args:
            a, b: First fraction (a/b)
            c, d: Second fraction (c/d)
            
        Returns:
            Result as decimal
        """
        try:
            result = Fraction(int(a), int(b)) / Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    # ==================== NUMBER THEORY CALCULATORS ====================
    
    @staticmethod
    def gcd(a: float, b: float) -> float:
        """
        Calculate GCD using Euclidean algorithm
        
        Args:
            a, b: Two numbers
            
        Returns:
            Greatest common divisor
        """
        try:
            return float(math.gcd(int(abs(a)), int(abs(b))))
        except Exception as e:
            return 1.0
    
    @staticmethod
    def lcm(a: float, b: float) -> float:
        """
        Calculate LCM: lcm(a,b) = (a × b) / gcd(a,b)
        
        Args:
            a, b: Two numbers
            
        Returns:
            Least common multiple
        """
        try:
            a_int = int(abs(a))
            b_int = int(abs(b))
            return float(abs(a_int * b_int) // math.gcd(a_int, b_int))
        except Exception as e:
            return 0.0
    
    @staticmethod
    def simplify_ratio(a: float, b: float) -> Tuple[float, float]:
        """
        Simplify ratio a:b
        
        Args:
            a, b: Ratio components
            
        Returns:
            Simplified ratio as tuple
        """
        try:
            gcd_val = math.gcd(int(abs(a)), int(abs(b)))
            return (float(int(a) // gcd_val), float(int(b) // gcd_val))
        except Exception as e:
            return (0.0, 0.0)
    
    # ==================== GROWTH CALCULATORS ====================
    
    @staticmethod
    def exponential_growth(x0: float, rate: float, time: float) -> float:
        """
        Calculate exponential growth: x(t) = x₀ × (1 + r)^t
        
        Args:
            x0: Initial value
            rate: Growth rate (as decimal, e.g., 0.05 for 5%)
            time: Time period
            
        Returns:
            Value after growth
        """
        try:
            return x0 * (1 + rate) ** time
        except Exception as e:
            return 0.0
    
    # ==================== RANDOM NUMBER GENERATOR ====================
    
    @staticmethod
    def generate_random(min_val: float, max_val: float, secure: bool = False) -> float:
        """
        Generate random number in range [min_val, max_val]
        secure=True uses cryptographically secure random
        
        Args:
            min_val: Minimum value
            max_val: Maximum value
            secure: Use secure random if True
            
        Returns:
            Random number
        """
        try:
            if secure:
                return secrets.SystemRandom().uniform(min_val, max_val)
            return random.uniform(min_val, max_val)
        except Exception as e:
            return 0.0
    
    # ==================== BASIC ARITHMETIC CALCULATORS ====================
    
    @staticmethod
    def add(a: float, b: float) -> float:
        """Basic addition"""
        try:
            return a + b
        except Exception as e:
            return 0.0
    
    @staticmethod
    def subtract(a: float, b: float) -> float:
        """Basic subtraction"""
        try:
            return a - b
        except Exception as e:
            return 0.0
    
    @staticmethod
    def multiply(a: float, b: float) -> float:
        """Basic multiplication"""
        try:
            return a * b
        except Exception as e:
            return 0.0
    
    @staticmethod
    def divide(a: float, b: float) -> Tuple[float, float]:
        """
        Basic division with remainder
        
        Args:
            a: Dividend
            b: Divisor
            
        Returns:
            Tuple of (quotient, remainder)
        """
        try:
            if b == 0:
                return (0.0, 0.0)
            quotient = float(a // b)
            remainder = float(a % b)
            return (quotient, remainder)
        except Exception as e:
            return (0.0, 0.0)


class FeatureEngineering:
    """
    Feature engineering class that applies mathematical calculators 
    to create new features for ML models
    """
    
    def __init__(self, dataframe):
        """
        Initialize with pandas DataFrame
        
        Args:
            dataframe: Input DataFrame with numerical features
        """
        self.df = dataframe.copy()
        self.calc = MathCalculators()
    
    def apply_all_calculators(self):
        """
        Apply all mathematical calculators as features to dataset
        Creates derived features from existing numerical columns
        
        Returns:
            DataFrame with additional calculator-based features
        """
        try:
            # Get numeric columns only
            numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
            
            if len(numeric_cols) < 2:
                return self.df
            
            # Statistical features (row-wise calculations)
            print("Adding statistical features...")
            self.df['row_variance'] = self.df[numeric_cols].apply(
                lambda row: self.calc.calculate_variance(row.values), axis=1
            )
            self.df['row_std'] = self.df[numeric_cols].apply(
                lambda row: self.calc.standard_deviation(row.values), axis=1
            )
            self.df['row_mean'] = self.df[numeric_cols].apply(
                lambda row: self.calc.mean(row.values), axis=1
            )
            
            # Logarithmic features (on positive values)
            print("Adding logarithmic features...")
            for col in numeric_cols[:3]:  # Apply to first 3 columns
                self.df[f'{col}_log'] = self.df[col].apply(
                    lambda x: self.calc.natural_log(abs(x) + 1)
                )
                self.df[f'{col}_log10'] = self.df[col].apply(
                    lambda x: self.calc.logarithm(abs(x) + 1, 10)
                )
            
            # Square root features
            print("Adding square root features...")
            for col in numeric_cols[:3]:
                self.df[f'{col}_sqrt'] = self.df[col].apply(
                    lambda x: self.calc.square_root(abs(x))
                )
            
            # Exponential features
            print("Adding exponential features...")
            for col in numeric_cols[:2]:
                self.df[f'{col}_exp'] = self.df[col].apply(
                    lambda x: self.calc.exponent(abs(x) + 1, 0.5)
                )
            
            # Trigonometric features (normalized to [-1, 1] range)
            print("Adding trigonometric features...")
            for col in numeric_cols[:2]:
                normalized = (self.df[col] - self.df[col].min()) / (self.df[col].max() - self.df[col].min() + 1e-10)
                angle = normalized * 360  # Scale to degrees
                self.df[f'{col}_sin'] = angle.apply(lambda x: self.calc.sine(x))
                self.df[f'{col}_cos'] = angle.apply(lambda x: self.calc.cosine(x))
            
            # Pairwise features (between first two columns)
            if len(numeric_cols) >= 2:
                print("Adding pairwise features...")
                col1, col2 = numeric_cols[0], numeric_cols[1]
                
                # Percentage change
                self.df[f'{col1}_{col2}_pct_change'] = self.df.apply(
                    lambda row: self.calc.percentage_change(
                        row[col1] if row[col1] != 0 else 0.001, 
                        row[col2]
                    ), axis=1
                )
                
                # Ratio
                self.df[f'{col1}_{col2}_ratio'] = self.df.apply(
                    lambda row: row[col1] / (row[col2] + 1e-10), axis=1
                )
                
                # GCD and LCM (on absolute integer values)
                self.df[f'{col1}_{col2}_gcd'] = self.df.apply(
                    lambda row: self.calc.gcd(abs(row[col1]), abs(row[col2])), axis=1
                )
                
                self.df[f'{col1}_{col2}_lcm'] = self.df.apply(
                    lambda row: self.calc.lcm(abs(row[col1]), abs(row[col2])), axis=1
                )
                
                # Pythagorean distance
                self.df[f'{col1}_{col2}_pythag'] = self.df.apply(
                    lambda row: self.calc.pythagorean(abs(row[col1]), abs(row[col2])), axis=1
                )
            
            # Polynomial features
            print("Adding polynomial features...")
            for col in numeric_cols[:2]:
                self.df[f'{col}_squared'] = self.df[col] ** 2
                self.df[f'{col}_cubed'] = self.df[col] ** 3
            
            # Replace any inf or nan values with 0
            self.df.replace([np.inf, -np.inf], 0, inplace=True)
            self.df.fillna(0, inplace=True)
            
            print(f"Feature engineering complete! Added {len(self.df.columns) - len(numeric_cols)} new features")
            return self.df
            
        except Exception as e:
            print(f"Error in feature engineering: {e}")
            return self.df
    
    def get_feature_names(self):
        """
        Get list of all feature names
        
        Returns:
            List of column names
        """
        return self.df.columns.tolist()
    
    def get_numeric_features(self):
        """
        Get list of numeric feature names
        
        Returns:
            List of numeric column names
        """
        return self.df.select_dtypes(include=[np.number]).columns.tolist()
