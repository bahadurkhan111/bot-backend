from rest_framework import serializers
from .models import NumberProperty


class NumberPropertySerializer(serializers.ModelSerializer):
    """Serializer for NumberProperty model."""
    
    sequences = serializers.SerializerMethodField()
    positions = serializers.SerializerMethodField()
    divisors = serializers.SerializerMethodField()
    conversions = serializers.SerializerMethodField()
    
    class Meta:
        model = NumberProperty
        fields = [
            'number',
            'condensed_number',
            'sequences',
            'positions',
            'divisors',
            'conversions',
            'natural_logarithm',
            'source_url',
            'scraped_at',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_sequences(self, obj):
        """Return sequence membership information."""
        return {
            'prime': obj.is_prime,
            'composite': obj.is_composite,
            'fibonacci': obj.is_fibonacci,
            'triangular': obj.is_triangular,
            'square': obj.is_square,
            'cube': obj.is_cube,
            'tetrahedral': obj.is_tetrahedral,
            'square_pyramidal': obj.is_square_pyramidal,
            'star': obj.is_star,
            'pentagonal': obj.is_pentagonal,
        }
    
    def get_positions(self, obj):
        """Return positions in sequences."""
        return {
            'prime': obj.prime_position,
            'composite': obj.composite_position,
            'fibonacci': obj.fibonacci_position,
            'triangular': obj.triangular_position,
            'square': obj.square_position,
            'cube': obj.cube_position,
            'tetrahedral': obj.tetrahedral_position,
            'square_pyramidal': obj.square_pyramidal_position,
            'star': obj.star_position,
            'pentagonal': obj.pentagonal_position,
        }
    
    def get_divisors(self, obj):
        """Return divisor information."""
        return {
            'count': obj.divisors_count,
            'sum': obj.divisors_sum,
            'list': obj.divisors_list,
        }
    
    def get_conversions(self, obj):
        """Return number conversions."""
        return {
            'binary': obj.conversion_binary,
            'octal': obj.conversion_octal,
            'duodecimal': obj.conversion_duodecimal,
            'hexadecimal': obj.conversion_hexadecimal,
            'roman': obj.roman_numeral,
        }


class NumberPropertySimpleSerializer(serializers.ModelSerializer):
    """Simplified serializer for quick lookups."""
    
    class Meta:
        model = NumberProperty
        fields = ['number', 'condensed_number', 'is_prime', 'is_composite']
