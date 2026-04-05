from django.contrib import admin
from .models import DateNumerology


@admin.register(DateNumerology)
class DateNumerologyAdmin(admin.ModelAdmin):
    """Admin interface for Date Numerology."""
    
    list_display = [
        'date', 'num1', 'num2', 'num3', 'num6', 'num8', 'created_at'
    ]
    list_filter = ['created_at']
    search_fields = ['date']
    readonly_fields = [
        'num1', 'num2', 'num3', 'num4', 'num5', 'num6',
        'num7', 'num8', 'num9', 'num10', 'num11', 'num12', 'num13',
        'numerologies_json', 'created_at', 'updated_at'
    ]
    
    fieldsets = (
        ('Date', {
            'fields': ('date',)
        }),
        ('Primary Numerologies (1-5)', {
            'fields': ('num1', 'num2', 'num3', 'num4', 'num5')
        }),
        ('Day-Based Numerologies (6-8)', {
            'fields': ('num6', 'num7', 'num8')
        }),
        ('Advanced Numerologies (9-11)', {
            'fields': ('num9', 'num10', 'num11')
        }),
        ('Product Numerologies (12-13)', {
            'fields': ('num12', 'num13')
        }),
        ('JSON Data', {
            'fields': ('numerologies_json',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
