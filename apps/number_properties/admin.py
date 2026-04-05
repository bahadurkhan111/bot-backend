from django.contrib import admin
from .models import NumberProperty


@admin.register(NumberProperty)
class NumberPropertyAdmin(admin.ModelAdmin):
    """Admin interface for Number Properties."""
    
    list_display = [
        'number', 'condensed_number', 'is_prime', 'is_composite', 
        'is_fibonacci', 'divisors_count', 'created_at'
    ]
    list_filter = ['is_prime', 'is_composite', 'is_fibonacci', 'is_square']
    search_fields = ['number']
    readonly_fields = [
        'condensed_number', 'properties_json', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Basic Info', {
            'fields': ('number', 'condensed_number')
        }),
        ('Sequence Membership', {
            'fields': (
                'is_prime', 'is_composite', 'is_fibonacci', 'is_triangular',
                'is_square', 'is_cube', 'is_tetrahedral', 'is_square_pyramidal',
                'is_star', 'is_pentagonal'
            )
        }),
        ('Sequence Positions', {
            'fields': (
                'prime_position', 'composite_position', 'fibonacci_position',
                'triangular_position', 'square_position', 'cube_position'
            ),
            'classes': ('collapse',)
        }),
        ('Divisors', {
            'fields': ('divisors_count', 'divisors_sum', 'divisors_list'),
            'classes': ('collapse',)
        }),
        ('Conversions', {
            'fields': (
                'conversion_binary', 'conversion_octal', 
                'conversion_hexadecimal', 'roman_numeral'
            ),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('source_url', 'scraped_at', 'properties_json', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
