# -*- coding: utf-8 -*-
"""
SECTION 2: MATHEMATICAL CALCULATORS CLASS
35 Mathematical calculators for feature engineering
"""

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
        except Exception as e:
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
        except Exception as e:
            return 0.0
    
    @staticmethod
    def mean(data: Union[list, np.ndarray]) -> float:
        """Calculate arithmetic mean"""
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
        """Calculate weighted average"""
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
        """Calculate percentage error"""
        try:
            if exact == 0:
                return 0.0
            return abs(exact - approx) / abs(exact) * 100
        except Exception as e:
            return 0.0
    
    @staticmethod
    def percentage_increase(initial: float, final: float) -> float:
        """Calculate percentage increase"""
        try:
            if initial == 0:
                return 0.0
            return ((final - initial) / initial) * 100
        except Exception as e:
            return 0.0
    
    @staticmethod
    def percentage(x: float, y: float) -> float:
        """Calculate x% of y"""
        try:
            return (x / 100) * y
        except Exception as e:
            return 0.0
    
    @staticmethod
    def percentage_change(old: float, new: float) -> float:
        """Calculate percentage change"""
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
        """Solve right triangle using Pythagorean theorem"""
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
        """Calculate square root"""
        try:
            if x < 0:
                return 0.0
            return math.sqrt(x)
        except Exception as e:
            return 0.0
    
    # ==================== LOGARITHMIC CALCULATORS ====================
    
    @staticmethod
    def natural_log(x: float) -> float:
        """Calculate natural logarithm"""
        try:
            if x <= 0:
                return 0.0
            return math.log(x)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def logarithm(x: float, base: float = 10) -> float:
        """Calculate logarithm with any base"""
        try:
            if x <= 0 or base <= 0 or base == 1:
                return 0.0
            return math.log(x, base)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def antilog(y: float, base: float = 10) -> float:
        """Calculate antilog"""
        try:
            if base == math.e:
                return math.exp(y)
            return base ** y
        except Exception as e:
            return 0.0
    
    # ==================== TRIGONOMETRIC CALCULATORS ====================
    
    @staticmethod
    def sine(angle: float, degrees: bool = True) -> float:
        """Calculate sine of angle"""
        try:
            if degrees:
                angle = math.radians(angle)
            return math.sin(angle)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def cosine(angle: float, degrees: bool = True) -> float:
        """Calculate cosine of angle"""
        try:
            if degrees:
                angle = math.radians(angle)
            return math.cos(angle)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def tangent(angle: float, degrees: bool = True) -> float:
        """Calculate tangent of angle"""
        try:
            if degrees:
                angle = math.radians(angle)
            return math.tan(angle)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def arcsine(x: float, degrees: bool = True) -> float:
        """Calculate inverse sine"""
        try:
            if x < -1 or x > 1:
                return 0.0
            result = math.asin(x)
            return math.degrees(result) if degrees else result
        except Exception as e:
            return 0.0
    
    @staticmethod
    def arccosine(x: float, degrees: bool = True) -> float:
        """Calculate inverse cosine"""
        try:
            if x < -1 or x > 1:
                return 0.0
            result = math.acos(x)
            return math.degrees(result) if degrees else result
        except Exception as e:
            return 0.0
    
    @staticmethod
    def arctangent(x: float, degrees: bool = True) -> float:
        """Calculate inverse tangent"""
        try:
            result = math.atan(x)
            return math.degrees(result) if degrees else result
        except Exception as e:
            return 0.0
    
    # ==================== ALGEBRAIC CALCULATORS ====================
    
    @staticmethod
    def factorial(n: float) -> float:
        """Calculate factorial"""
        try:
            if n < 0:
                return 0.0
            return float(math.factorial(int(n)))
        except Exception as e:
            return 0.0
    
    @staticmethod
    def exponent(base: float, power: float) -> float:
        """Calculate base^power"""
        try:
            return base ** power
        except Exception as e:
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
        except Exception as e:
            return (0.0, 0.0)
    
    # ==================== FRACTION CALCULATORS ====================
    
    @staticmethod
    def add_fractions(a: float, b: float, c: float, d: float) -> float:
        """Add fractions: a/b + c/d"""
        try:
            result = Fraction(int(a), int(b)) + Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def subtract_fractions(a: float, b: float, c: float, d: float) -> float:
        """Subtract fractions: a/b - c/d"""
        try:
            result = Fraction(int(a), int(b)) - Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def multiply_fractions(a: float, b: float, c: float, d: float) -> float:
        """Multiply fractions: (a/b) × (c/d)"""
        try:
            result = Fraction(int(a), int(b)) * Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    @staticmethod
    def divide_fractions(a: float, b: float, c: float, d: float) -> float:
        """Divide fractions: (a/b) ÷ (c/d)"""
        try:
            result = Fraction(int(a), int(b)) / Fraction(int(c), int(d))
            return float(result)
        except Exception as e:
            return 0.0
    
    # ==================== NUMBER THEORY CALCULATORS ====================
    
    @staticmethod
    def gcd(a: float, b: float) -> float:
        """Calculate GCD using Euclidean algorithm"""
        try:
            return float(math.gcd(int(abs(a)), int(abs(b))))
        except Exception as e:
            return 1.0
    
    @staticmethod
    def lcm(a: float, b: float) -> float:
        """Calculate LCM"""
        try:
            a_int = int(abs(a))
            b_int = int(abs(b))
            return float(abs(a_int * b_int) // math.gcd(a_int, b_int))
        except Exception as e:
            return 0.0
    
    @staticmethod
    def simplify_ratio(a: float, b: float) -> Tuple[float, float]:
        """Simplify ratio a:b"""
        try:
            gcd_val = math.gcd(int(abs(a)), int(abs(b)))
            return (float(int(a) // gcd_val), float(int(b) // gcd_val))
        except Exception as e:
            return (0.0, 0.0)
    
    # ==================== GROWTH CALCULATORS ====================
    
    @staticmethod
    def exponential_growth(x0: float, rate: float, time: float) -> float:
        """Calculate exponential growth"""
        try:
            return x0 * (1 + rate) ** time
        except Exception as e:
            return 0.0
    
    # ==================== RANDOM NUMBER GENERATOR ====================
    
    @staticmethod
    def generate_random(min_val: float, max_val: float, secure: bool = False) -> float:
        """Generate random number in range"""
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
        """Basic division with remainder"""
        try:
            if b == 0:
                return (0.0, 0.0)
            quotient = float(a // b)
            remainder = float(a % b)
            return (quotient, remainder)
        except Exception as e:
            return (0.0, 0.0)

print("✓ MathCalculators class defined")
