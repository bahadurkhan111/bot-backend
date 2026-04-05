from django.db import models


class NumberProperty(models.Model):
    """
    Number properties from Gematrinator for days 1-31.
    
    Each number has various mathematical properties (prime, composite, fibonacci, etc.)
    and a 'condensed_number' which is the key value used in the prediction formula.
    """
    
    number = models.IntegerField(unique=True, db_index=True, primary_key=True)
    
    # Sequence membership (boolean flags)
    is_prime = models.BooleanField(default=False)
    is_composite = models.BooleanField(default=False)
    is_fibonacci = models.BooleanField(default=False)
    is_triangular = models.BooleanField(default=False)
    is_square = models.BooleanField(default=False)
    is_cube = models.BooleanField(default=False)
    is_tetrahedral = models.BooleanField(default=False)
    is_square_pyramidal = models.BooleanField(default=False)
    is_star = models.BooleanField(default=False)
    is_pentagonal = models.BooleanField(default=False)
    
    # Sequence positions (if member of sequence)
    prime_position = models.IntegerField(null=True, blank=True)
    composite_position = models.IntegerField(null=True, blank=True)
    fibonacci_position = models.IntegerField(null=True, blank=True)
    triangular_position = models.IntegerField(null=True, blank=True)
    square_position = models.IntegerField(null=True, blank=True)
    cube_position = models.IntegerField(null=True, blank=True)
    tetrahedral_position = models.IntegerField(null=True, blank=True)
    square_pyramidal_position = models.IntegerField(null=True, blank=True)
    star_position = models.IntegerField(null=True, blank=True)
    pentagonal_position = models.IntegerField(null=True, blank=True)
    
    # Nth values (what is the Nth prime, composite, etc.)
    prime_nth_value = models.IntegerField(null=True, blank=True)
    composite_nth_value = models.IntegerField(null=True, blank=True)
    fibonacci_nth_value = models.IntegerField(null=True, blank=True)
    triangular_nth_value = models.IntegerField(null=True, blank=True)
    square_nth_value = models.IntegerField(null=True, blank=True)
    cube_nth_value = models.IntegerField(null=True, blank=True)
    tetrahedral_nth_value = models.IntegerField(null=True, blank=True)
    square_pyramidal_nth_value = models.IntegerField(null=True, blank=True)
    star_nth_value = models.IntegerField(null=True, blank=True)
    pentagonal_nth_value = models.IntegerField(null=True, blank=True)
    
    # Divisor properties
    divisors_count = models.IntegerField(null=True, blank=True)
    divisors_sum = models.IntegerField(null=True, blank=True)
    divisors_list = models.JSONField(null=True, blank=True)
    
    # Number conversions
    conversion_binary = models.CharField(max_length=50, blank=True)
    conversion_octal = models.CharField(max_length=50, blank=True)
    conversion_duodecimal = models.CharField(max_length=50, blank=True)
    conversion_hexadecimal = models.CharField(max_length=50, blank=True)
    roman_numeral = models.CharField(max_length=50, blank=True)
    
    # Mathematical properties
    natural_logarithm = models.FloatField(null=True, blank=True)
    
    # THE KEY VALUE FOR FORMULA
    condensed_number = models.IntegerField(
        help_text="The core numerological value used in prediction formula"
    )
    
    # Pd value from Gematrinator (sides of shapes or position in sequences)
    pd_value = models.IntegerField(
        null=True,
        blank=True,
        help_text="Pd value: number of sides for geometric shapes, position for numeric sequences"
    )
    
    # Primary sequence name from Gematrinator
    primary_sequence = models.CharField(
        max_length=100,
        blank=True,
        help_text="Primary highlighted sequence from Gematrinator"
    )
    
    # Store full properties as JSON for reference
    properties_json = models.JSONField(default=dict, blank=True)
    
    # Metadata
    source_url = models.URLField(blank=True)
    scraped_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'number_properties'
        verbose_name = 'Number Property'
        verbose_name_plural = 'Number Properties'
        ordering = ['number']
    
    def __str__(self):
        return f"Number {self.number} (condensed: {self.condensed_number})"
    
    @classmethod
    def get_pd_value(cls, day: int) -> int:
        """
        Get the Pd value for a given day (1-31).
        
        Pd value is calculated from Gematrinator sequences:
        - Geometric shapes → Number of sides/faces
        - Numeric sequences → Position in sequence
        
        Args:
            day: Day of month (1-31)
            
        Returns:
            The Pd value for that day
            
        Raises:
            ValueError: If day is outside 1-31 range
            cls.DoesNotExist: If number not found in database
        """
        if not 1 <= day <= 31:
            raise ValueError(f"Day must be between 1 and 31, got {day}")
        
        try:
            prop = cls.objects.get(number=day)
            return prop.pd_value if prop.pd_value is not None else prop.condensed_number
        except cls.DoesNotExist:
            raise cls.DoesNotExist(
                f"Number properties for day {day} not found in database. "
                "Run: python manage.py import_number_properties"
            )
    
    @classmethod
    def get_condensed_number(cls, day: int) -> int:
        """
        Get the condensed number for a given day (1-31).
        
        Args:
            day: Day of month (1-31)
            
        Returns:
            The condensed number for that day
            
        Raises:
            ValueError: If day is outside 1-31 range
            cls.DoesNotExist: If number not found in database
        """
        if not 1 <= day <= 31:
            raise ValueError(f"Day must be between 1 and 31, got {day}")
        
        try:
            prop = cls.objects.get(number=day)
            return prop.condensed_number
        except cls.DoesNotExist:
            raise cls.DoesNotExist(
                f"Number properties for day {day} not found in database. "
                "Run: python manage.py import_number_properties"
            )
    
    @classmethod
    def calculate_condensed_number(cls, number: int) -> int:
        """
        Calculate the condensed number (numerological reduction to single digit).
        
        This is a fallback calculation if the condensed number is not explicitly defined.
        It performs numerological reduction: sum digits repeatedly until single digit.
        
        Examples:
            14 -> 1+4 = 5
            28 -> 2+8 = 10 -> 1+0 = 1
            31 -> 3+1 = 4
        
        Args:
            number: The number to condense
            
        Returns:
            Single digit (1-9)
        """
        total = number
        while total >= 10:
            total = sum(int(d) for d in str(total))
        return total
    
    def to_dict(self):
        """Return number properties as dictionary."""
        return {
            'number': self.number,
            'condensed_number': self.condensed_number,
            'sequences': {
                'is_prime': self.is_prime,
                'is_composite': self.is_composite,
                'is_fibonacci': self.is_fibonacci,
                'is_triangular': self.is_triangular,
                'is_square': self.is_square,
                'is_cube': self.is_cube,
            },
            'positions': {
                'prime': self.prime_position,
                'composite': self.composite_position,
                'fibonacci': self.fibonacci_position,
                'triangular': self.triangular_position,
                'square': self.square_position,
            },
            'divisors': {
                'count': self.divisors_count,
                'sum': self.divisors_sum,
                'list': self.divisors_list,
            },
            'conversions': {
                'binary': self.conversion_binary,
                'octal': self.conversion_octal,
                'hexadecimal': self.conversion_hexadecimal,
                'roman': self.roman_numeral,
            }
        }
