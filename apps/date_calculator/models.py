from django.db import models
from django.utils import timezone


class DateNumerology(models.Model):
    """
    Cache calculated date numerologies for performance.
    Stores all 13 numerological values for each unique date.
    """
    
    date = models.DateField(unique=True, db_index=True)
    
    # 13 Numerology values
    num1 = models.IntegerField(help_text="Month + Day + Century + Decade")
    num2 = models.IntegerField(help_text="Month + Day + Year Digits Sum")
    num3 = models.IntegerField(help_text="All Digits Sum")
    num4 = models.IntegerField(help_text="Month + Day + Decade")
    num5 = models.IntegerField(help_text="Digits Without Century")
    num6 = models.IntegerField(help_text="Day of Year")
    num7 = models.IntegerField(help_text="Days Remaining in Year")
    num8 = models.IntegerField(help_text="Month + Day")
    num9 = models.IntegerField(help_text="Month Digits + Day Digits + Century + Decade")
    num10 = models.IntegerField(help_text="Month + Day + Decade Digits Sum")
    num11 = models.IntegerField(help_text="Month Digits + Day Digits + Decade")
    num12 = models.IntegerField(help_text="Product of All Digits with Full Year")
    num13 = models.IntegerField(help_text="Product of Digits with Last 2 Year Digits")
    
    # Store as JSON for easy API access
    numerologies_json = models.JSONField()
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'date_numerologies'
        verbose_name = 'Date Numerology'
        verbose_name_plural = 'Date Numerologies'
        ordering = ['-date']
    
    def __str__(self):
        return f"Numerologies for {self.date}"
    
    @classmethod
    def get_or_calculate(cls, date):
        """
        Get cached numerologies or calculate and cache them.
        
        Args:
            date: datetime.date or datetime.datetime object
            
        Returns:
            DateNumerology instance
        """
        from datetime import datetime
        from .calculator import DateCalculator
        
        # Convert datetime to date if needed
        if isinstance(date, datetime):
            date = date.date()
        
        # Try to get from cache
        try:
            return cls.objects.get(date=date)
        except cls.DoesNotExist:
            # Calculate and cache
            calculator = DateCalculator()
            numerologies = calculator.calculate_all(datetime.combine(date, datetime.min.time()))
            
            instance = cls.objects.create(
                date=date,
                num1=numerologies['num1'],
                num2=numerologies['num2'],
                num3=numerologies['num3'],
                num4=numerologies['num4'],
                num5=numerologies['num5'],
                num6=numerologies['num6'],
                num7=numerologies['num7'],
                num8=numerologies['num8'],
                num9=numerologies['num9'],
                num10=numerologies['num10'],
                num11=numerologies['num11'],
                num12=numerologies['num12'],
                num13=numerologies['num13'],
                numerologies_json=numerologies
            )
            return instance
    
    def to_dict(self):
        """Return numerologies as dictionary."""
        return {
            'date': self.date.isoformat(),
            'numerologies': {
                'num1': self.num1,
                'num2': self.num2,
                'num3': self.num3,
                'num4': self.num4,
                'num5': self.num5,
                'num6': self.num6,
                'num7': self.num7,
                'num8': self.num8,
                'num9': self.num9,
                'num10': self.num10,
                'num11': self.num11,
                'num12': self.num12,
                'num13': self.num13,
            },
            'numerologies_list': [
                self.num1, self.num2, self.num3, self.num4,
                self.num5, self.num6, self.num7, self.num8,
                self.num9, self.num10, self.num11, self.num12,
                self.num13
            ]
        }
