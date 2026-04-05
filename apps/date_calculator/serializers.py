from rest_framework import serializers
from .models import DateNumerology


class DateNumerologySerializer(serializers.ModelSerializer):
    """Serializer for DateNumerology model."""
    
    numerologies_list = serializers.SerializerMethodField()
    descriptions = serializers.SerializerMethodField()
    
    class Meta:
        model = DateNumerology
        fields = [
            'date',
            'num1', 'num2', 'num3', 'num4', 'num5',
            'num6', 'num7', 'num8', 'num9', 'num10',
            'num11', 'num12', 'num13',
            'numerologies_list',
            'numerologies_json',
            'descriptions',
            'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_numerologies_list(self, obj):
        """Return numerologies as a simple list."""
        return [
            obj.num1, obj.num2, obj.num3, obj.num4, obj.num5,
            obj.num6, obj.num7, obj.num8, obj.num9, obj.num10,
            obj.num11, obj.num12, obj.num13
        ]
    
    def get_descriptions(self, obj):
        """Return descriptions for each numerology."""
        from .calculator import DateCalculator
        return DateCalculator.get_numerology_descriptions()


class DateNumerologyCalculateSerializer(serializers.Serializer):
    """Serializer for calculating numerologies from a date string."""
    
    date = serializers.DateField(
        required=True,
        help_text="Date in YYYY-MM-DD format"
    )
    
    def validate_date(self, value):
        """Validate the date."""
        return value
