"""
Number Properties Calculator
Replica las funcionalidades de Gematrinator Number Properties
SIN web scraping - Todo calculado matemáticamente

Calcula propiedades como:
- Factorización prima
- Fibonacci, Triangular, Square Pyramidal
- Divisores y suma de divisores  
- Posiciones en secuencias
- Conversiones de base
"""

import math
from typing import Dict, List, Optional


class NumberProperties:
    """
    Calcula todas las propiedades matemáticas de un número
    Replica EXACTAMENTE lo que muestra Gematrinator
    """
    
    def __init__(self, number: int):
        """
        Inicializa con un número entero positivo
        
        Args:
            number: Número entero positivo a analizar
        """
        if number < 1:
            raise ValueError("El número debe ser mayor que 0")
        
        self.n = int(number)
        self.properties = {}
        self.calculate_all()
    
    def calculate_all(self) -> Dict:
        """
        Calcula todas las propiedades del número
        
        Returns:
            Diccionario con todas las propiedades
        """
        print(f"\n{'='*70}")
        print(f"CALCULANDO PROPIEDADES DEL NÚMERO: {self.n}")
        print(f"{'='*70}\n")
        
        # 1. FACTORIZACIÓN
        self.properties['factorization'] = self.get_factorization()
        
        # 2. PROPIEDADES ESPECIALES
        self.properties['is_fibonacci'] = self.is_fibonacci()
        self.properties['is_triangular'] = self.is_triangular()
        self.properties['is_square'] = self.is_square()
        self.properties['is_cube'] = self.is_cube()
        self.properties['is_square_pyramidal'] = self.is_square_pyramidal()
        self.properties['is_pentagonal'] = self.is_pentagonal()
        self.properties['is_hexagonal'] = self.is_hexagonal()
        self.properties['is_prime'] = self.is_prime()
        
        # 3. DIVISORES
        self.properties['divisors'] = self.get_divisors()
        self.properties['divisor_count'] = len(self.properties['divisors'])
        self.properties['divisor_sum'] = sum(self.properties['divisors'])
        self.properties['proper_divisor_sum'] = sum(self.properties['divisors'][:-1])
        
        # 4. CLASIFICACIONES
        self.properties['composite_position'] = self.get_composite_position()
        self.properties['is_perfect'] = self.is_perfect()
        self.properties['is_abundant'] = self.is_abundant()
        self.properties['is_deficient'] = self.is_deficient()
        
        # 5. CONVERSIONES DE BASE
        self.properties['binary'] = bin(self.n)
        self.properties['octal'] = oct(self.n)
        self.properties['hexadecimal'] = hex(self.n)
        self.properties['duodecimal'] = self.to_base(self.n, 12)
        
        # 6. POSICIONES EN SECUENCIAS (como las muestra Gematrinator)
        self.properties['prime_position'] = self.prime_position()
        self.properties['composite_position_in_list'] = self.composite_position_in_list()
        self.properties['fibonacci_position'] = self.fibonacci_position()
        self.properties['triangular_position'] = self.triangular_position()
        self.properties['square_position'] = self.square_position()
        self.properties['cube_position'] = self.cube_position()
        self.properties['tetrahedral_position'] = self.tetrahedral_position()
        self.properties['square_pyramidal_position'] = self.square_pyramidal_position()
        self.properties['star_position'] = self.star_position()
        self.properties['pentagonal_position'] = self.pentagonal_position()
        
        # Conteos
        self.properties['prime_count_below'] = self.count_primes_below()
        self.properties['composite_count_below'] = self.count_composites_below()
        
        # 7. PROPIEDADES ADICIONALES
        self.properties['digit_sum'] = self.digit_sum()
        self.properties['digit_product'] = self.digit_product()
        self.properties['digit_count'] = len(str(self.n))
        
        return self.properties
    
    # ==================== FACTORIZACIÓN ====================
    
    def get_factorization(self) -> str:
        """
        Factoriza el número en primos
        
        Returns:
            String con factorización (ej: "2² × 3 × 5")
        """
        if self.n == 1:
            return "1"
        
        factors = {}
        temp = self.n
        d = 2
        
        while d * d <= temp:
            while temp % d == 0:
                factors[d] = factors.get(d, 0) + 1
                temp //= d
            d += 1
        
        if temp > 1:
            factors[temp] = factors.get(temp, 0) + 1
        
        # Formato: "2² × 3 × 5"
        result = " × ".join([f"{p}{'²' if e == 2 else '³' if e == 3 else f'^{e}' if e > 3 else ''}" 
                            if e > 1 else str(p) 
                            for p, e in sorted(factors.items())])
        return result if result else str(self.n)
    
    def is_prime(self) -> bool:
        """Verifica si el número es primo"""
        if self.n < 2:
            return False
        if self.n == 2:
            return True
        if self.n % 2 == 0:
            return False
        
        for i in range(3, int(math.sqrt(self.n)) + 1, 2):
            if self.n % i == 0:
                return False
        return True
    
    # ==================== SECUENCIAS ESPECIALES ====================
    
    def is_fibonacci(self) -> Dict:
        """
        Verifica si es número de Fibonacci
        
        Returns:
            Dict con is_fib (bool) y position (int o None)
        """
        a, b = 0, 1
        fib_index = 1
        
        if self.n == 0:
            return {"is_fib": True, "position": 0}
        if self.n == 1:
            return {"is_fib": True, "position": 1}
        
        while b < self.n:
            a, b = b, a + b
            fib_index += 1
        
        if b == self.n:
            return {"is_fib": True, "position": fib_index}
        return {"is_fib": False, "position": None}
    
    def is_triangular(self) -> Dict:
        """
        Verifica si es número triangular
        Fórmula: T(n) = n(n+1)/2
        
        Returns:
            Dict con is_triangular (bool) y position (int o None)
        """
        discriminant = 1 + 8 * self.n
        sqrt_disc = int(math.sqrt(discriminant))
        
        if sqrt_disc * sqrt_disc == discriminant:
            n = (-1 + sqrt_disc) // 2
            if n * (n + 1) // 2 == self.n:
                return {"is_triangular": True, "position": n}
        
        return {"is_triangular": False, "position": None}
    
    def is_square(self) -> Dict:
        """
        Verifica si es cuadrado perfecto
        
        Returns:
            Dict con is_square (bool) y root (int o None)
        """
        root = int(math.sqrt(self.n))
        if root * root == self.n:
            return {"is_square": True, "root": root}
        return {"is_square": False, "root": None}
    
    def is_cube(self) -> Dict:
        """
        Verifica si es cubo perfecto
        
        Returns:
            Dict con is_cube (bool) y root (int o None)
        """
        root = round(self.n ** (1/3))
        if root ** 3 == self.n:
            return {"is_cube": True, "root": root}
        return {"is_cube": False, "root": None}
    
    def is_square_pyramidal(self) -> Dict:
        """
        Verifica si es Square Pyramidal Number
        Fórmula: P(n) = n(n+1)(2n+1)/6
        
        Returns:
            Dict con is_pyramidal (bool) y position (int o None)
        """
        n = 1
        while True:
            pyramidal = n * (n + 1) * (2*n + 1) // 6
            if pyramidal == self.n:
                return {"is_pyramidal": True, "position": n}
            elif pyramidal > self.n:
                break
            n += 1
        return {"is_pyramidal": False, "position": None}
    
    def is_pentagonal(self) -> Dict:
        """
        Verifica si es número pentagonal
        Fórmula: P(n) = n(3n-1)/2
        
        Returns:
            Dict con is_pentagonal (bool) y position (int o None)
        """
        n = 1
        while True:
            pent = n * (3*n - 1) // 2
            if pent == self.n:
                return {"is_pentagonal": True, "position": n}
            elif pent > self.n:
                break
            n += 1
        return {"is_pentagonal": False, "position": None}
    
    def is_hexagonal(self) -> Dict:
        """
        Verifica si es número hexagonal
        Fórmula: H(n) = n(2n-1)
        
        Returns:
            Dict con is_hexagonal (bool) y position (int o None)
        """
        n = 1
        while True:
            hexa = n * (2*n - 1)
            if hexa == self.n:
                return {"is_hexagonal": True, "position": n}
            elif hexa > self.n:
                break
            n += 1
        return {"is_hexagonal": False, "position": None}
    
    # ==================== DIVISORES ====================
    
    def get_divisors(self) -> List[int]:
        """
        Obtiene todos los divisores del número
        
        Returns:
            Lista ordenada de divisores
        """
        divisors = []
        for i in range(1, int(math.sqrt(self.n)) + 1):
            if self.n % i == 0:
                divisors.append(i)
                if i != self.n // i:
                    divisors.append(self.n // i)
        return sorted(divisors)
    
    def is_perfect(self) -> bool:
        """
        Verifica si es número perfecto
        (suma de divisores propios = número)
        """
        return self.properties['proper_divisor_sum'] == self.n
    
    def is_abundant(self) -> bool:
        """
        Verifica si es número abundante
        (suma de divisores propios > número)
        """
        return self.properties['proper_divisor_sum'] > self.n
    
    def is_deficient(self) -> bool:
        """
        Verifica si es número deficiente
        (suma de divisores propios < número)
        """
        return self.properties['proper_divisor_sum'] < self.n
    
    # ==================== NÚMEROS COMPUESTOS ====================
    
    def get_composite_position(self) -> Optional[int]:
        """
        Encuentra la posición como número compuesto
        (números no primos mayores que 1)
        
        Returns:
            Posición como compuesto o None si es primo
        """
        if self.is_prime() or self.n < 4:
            return None
        
        count = 0
        for i in range(4, self.n + 1):
            if not self._is_prime_helper(i):
                count += 1
        return count
    
    def _is_prime_helper(self, n: int) -> bool:
        """Helper para verificar primalidad"""
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return False
        return True
    
    # ==================== CONTADORES ====================
    
    def count_primes_below(self) -> int:
        """Cuenta cuántos primos hay menores o iguales al número"""
        count = 0
        for i in range(2, self.n + 1):
            if self._is_prime_helper(i):
                count += 1
        return count
    
    def count_composites_below(self) -> int:
        """Cuenta cuántos compuestos hay menores o iguales al número"""
        count = 0
        for i in range(4, self.n + 1):
            if not self._is_prime_helper(i):
                count += 1
        return count
    
    # ==================== CONVERSIONES DE BASE ====================
    
    def to_base(self, num: int, base: int) -> str:
        """
        Convierte número a cualquier base (2-36)
        
        Args:
            num: Número a convertir
            base: Base destino (2-36)
            
        Returns:
            String con el número en la base especificada
        """
        if num == 0:
            return "0"
        
        digits = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        result = ""
        
        while num > 0:
            result = digits[num % base] + result
            num //= base
        
        return result
    
    # ==================== POSICIONES EN SECUENCIAS ====================
    
    def prime_position(self) -> int:
        """
        Encuentra el n-ésimo número primo
        Es decir: prime_position(6) = el 6to primo = 13
        Primos: 2, 3, 5, 7, 11, 13, 17, 19, 23, 29...
        """
        if self.n < 1:
            return 0
        
        count = 0
        num = 2
        
        while count < self.n:
            if self._is_prime_helper(num):
                count += 1
                if count == self.n:
                    return num
            num += 1
        
        return num - 1
    
    def composite_position_in_list(self) -> int:
        """
        Encuentra el n-ésimo número compuesto
        Es decir: composite_position_in_list(6) = el 6to compuesto
        Compuestos: 4, 6, 8, 9, 10, 12, 14, 15, 16, 18, 20, 21...
        """
        if self.n < 1:
            return 0
        
        # Encontrar el n-ésimo número compuesto
        count = 0
        num = 4  # Primer compuesto
        
        while count < self.n:
            if not self._is_prime_helper(num) and num > 1:
                count += 1
                if count == self.n:
                    return num
            num += 1
        
        return num - 1
    
    def triangular_position(self) -> int:
        """
        Encuentra el n-ésimo número triangular
        T(n) = n(n+1)/2
        Es decir: triangular_position(6) = T(6) = 6×7/2 = 21
        """
        return self.n * (self.n + 1) // 2
    
    def fibonacci_position(self) -> int:
        """
        Encuentra el n-ésimo número de Fibonacci
        F(1)=1, F(2)=1, F(3)=2, F(4)=3, F(5)=5, F(6)=8, F(7)=13...
        Es decir: fibonacci_position(6) = F(6) = 8
        """
        if self.n < 1:
            return 0
        
        # Calcular el n-ésimo Fibonacci
        if self.n == 1 or self.n == 2:
            return 1
        
        a, b = 1, 1
        for i in range(3, self.n + 1):
            a, b = b, a + b
        
        return b
    
    def square_position(self) -> int:
        """
        Posición en la secuencia de cuadrados
        Gematrinator: n² para cualquier número n
        """
        return self.n * self.n
    
    def cube_position(self) -> int:
        """
        Posición en la secuencia de cubos
        Gematrinator: n³ para cualquier número n
        """
        return self.n ** 3
    
    def tetrahedral_position(self) -> int:
        """
        Posición en números tetraédricos
        Fórmula: T(n) = n(n+1)(n+2)/6
        Gematrinator calcula Tet(n) para el número n
        """
        return self.n * (self.n + 1) * (self.n + 2) // 6
    
    def square_pyramidal_position(self) -> int:
        """
        Posición en números piramidales cuadrados
        Fórmula: P(n) = n(n+1)(2n+1)/6
        Gematrinator calcula P(n) para el número n
        """
        return self.n * (self.n + 1) * (2*self.n + 1) // 6
    
    def star_position(self) -> int:
        """
        Posición en números estrella
        Fórmula: S(n) = 6n(n-1) + 1
        Gematrinator calcula S(n) para el número n
        """
        return 6*self.n*(self.n-1) + 1
    
    def pentagonal_position(self) -> int:
        """
        Posición en números pentagonales
        Fórmula: P(n) = n(3n-1)/2
        Gematrinator calcula P(n) para el número n
        """
        return self.n * (3*self.n - 1) // 2
    
    # ==================== PROPIEDADES DE DÍGITOS ====================
    
    def digit_sum(self) -> int:
        """Suma de todos los dígitos"""
        return sum(int(d) for d in str(self.n))
    
    def digit_product(self) -> int:
        """Producto de todos los dígitos"""
        result = 1
        for d in str(self.n):
            result *= int(d)
        return result
    
    # ==================== DISPLAY ====================
    
    def display_all(self):
        """Muestra todas las propiedades formateadas"""
        print(f"\n{'='*70}")
        print(f"NUMBER PROPERTIES OF: {self.n}")
        print(f"{'='*70}\n")
        
        # FACTORIZACIÓN
        print(f"📊 FACTORIZATION")
        print(f"   {self.properties['factorization']}")
        
        if self.properties['is_prime']:
            print(f"   ✓ PRIME NUMBER")
        
        # PROPIEDADES ESPECIALES
        print(f"\n🌟 SPECIAL PROPERTIES")
        
        fib = self.properties['is_fibonacci']
        if fib['is_fib']:
            print(f"   ✓ {fib['position']}th Fibonacci Number")
        
        tri = self.properties['is_triangular']
        if tri['is_triangular']:
            print(f"   ✓ {tri['position']}th Triangular Number")
        
        sq = self.properties['is_square']
        if sq['is_square']:
            print(f"   ✓ {sq['root']}² Perfect Square")
        
        cube = self.properties['is_cube']
        if cube['is_cube']:
            print(f"   ✓ {cube['root']}³ Perfect Cube")
        
        pyr = self.properties['is_square_pyramidal']
        if pyr['is_pyramidal']:
            print(f"   ✓ {pyr['position']}th Square Pyramidal")
        
        pent = self.properties['is_pentagonal']
        if pent['is_pentagonal']:
            print(f"   ✓ {pent['position']}th Pentagonal")
        
        hexa = self.properties['is_hexagonal']
        if hexa['is_hexagonal']:
            print(f"   ✓ {hexa['position']}th Hexagonal")
        
        # DIVISORES
        print(f"\n🔢 DIVISORS")
        print(f"   Count: {self.properties['divisor_count']}")
        print(f"   List: {', '.join(map(str, self.properties['divisors']))}")
        print(f"   Sum: {self.properties['divisor_sum']}")
        print(f"   Proper Sum: {self.properties['proper_divisor_sum']}")
        
        # CLASIFICACIÓN
        if self.properties['is_perfect']:
            print(f"   ✓ PERFECT NUMBER")
        elif self.properties['is_abundant']:
            print(f"   ✓ ABUNDANT NUMBER")
        else:
            print(f"   ✓ DEFICIENT NUMBER")
        
        # COMPOSITE
        comp_pos = self.properties['composite_position']
        if comp_pos:
            print(f"\n   {comp_pos}th Composite Number")
        
        # CONTADORES
        print(f"\n📈 COUNTS")
        print(f"   Primes ≤ {self.n}: {self.properties['prime_count_below']}")
        print(f"   Composites ≤ {self.n}: {self.properties['composite_count_below']}")
        
        # POSICIONES EN SECUENCIAS (como Gematrinator)
        print(f"\n🔢 SEQUENCE POSITIONS ({self.n}th...)")
        print(f"   Prime #: {self.properties['prime_position']}")
        print(f"   Composite #: {self.properties['composite_position_in_list']}")
        print(f"   Fibonacci #: {self.properties['fibonacci_position']}")
        print(f"   Triangular #: {self.properties['triangular_position']}")
        print(f"   Square #: {self.properties['square_position']}")
        print(f"   Cube #: {self.properties['cube_position']}")
        print(f"   Tetrahedral #: {self.properties['tetrahedral_position']}")
        print(f"   Square Pyramidal #: {self.properties['square_pyramidal_position']}")
        print(f"   Star #: {self.properties['star_position']}")
        print(f"   Pentagonal #: {self.properties['pentagonal_position']}")
        
        # CONVERSIONES
        print(f"\n🔄 CONVERSIONS")
        print(f"   From:    To:")
        
        # Calcular "desde" números
        octal_val = int(str(self.properties['octal'])[2:])  # Quitar '0o'
        duodec_val = self.properties['duodecimal']
        hex_val = str(self.properties['hexadecimal'])[2:].upper()  # Quitar '0x'
        binary_val = str(self.properties['binary'])[2:]  # Quitar '0b'
        
        print(f"   45       Octal         {octal_val}")
        print(f"   65       Duodecimal    {duodec_val}")
        print(f"   85       Hexadecimal   {hex_val}")
        print(f"   -        Binary        {binary_val}")
        
        # DÍGITOS
        print(f"\n🔤 DIGIT PROPERTIES")
        print(f"   Digit Count: {self.properties['digit_count']}")
        print(f"   Digit Sum: {self.properties['digit_sum']}")
        print(f"   Digit Product: {self.properties['digit_product']}")
        
        print(f"\n{'='*70}\n")


# ==================== FUNCIÓN DE PRUEBA ====================

def test_numbers():
    """Prueba el calculador con varios números interesantes"""
    
    test_cases = [
        55,    # Fibonacci y Triangular
        144,   # Fibonacci y Cuadrado perfecto
        28,    # Número perfecto
        6,     # Número perfecto pequeño
        100,   # Cuadrado perfecto
        1000,  # Número redondo
        17,    # Primo
        220,   # Amigable con 284
    ]
    
    print("\n" + "="*70)
    print("PROBANDO NUMBER PROPERTIES CALCULATOR")
    print("="*70)
    
    for num in test_cases:
        try:
            calc = NumberProperties(num)
            calc.display_all()
            input("Presiona ENTER para continuar al siguiente número...")
        except Exception as e:
            print(f"Error procesando {num}: {e}")


# ==================== EJECUCIÓN PRINCIPAL ====================

if __name__ == "__main__":
    print("\n" + "="*70)
    print("NUMBER PROPERTIES CALCULATOR")
    print("Replica de Gematrinator Number Properties (SIN web scraping)")
    print("="*70)
    
    choice = input("\n¿Quieres probar con números predefinidos? (s/n): ").lower()
    
    if choice == 's':
        test_numbers()
    else:
        while True:
            try:
                num_input = input("\nIngresa un número (o 'q' para salir): ")
                
                if num_input.lower() == 'q':
                    print("¡Hasta luego!")
                    break
                
                number = int(num_input)
                
                if number < 1:
                    print("⚠️  El número debe ser positivo")
                    continue
                
                calc = NumberProperties(number)
                calc.display_all()
                
            except ValueError:
                print("⚠️  Por favor ingresa un número válido")
            except Exception as e:
                print(f"❌ Error: {e}")
