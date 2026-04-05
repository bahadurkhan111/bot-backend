from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import NumberProperty
from .serializers import NumberPropertySerializer, NumberPropertySimpleSerializer


class NumberPropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Number Properties.
    
    Endpoints:
        GET /api/number-properties/ - List all number properties (1-31)
        GET /api/number-properties/{number}/ - Get properties for specific number
        GET /api/number-properties/{number}/condensed/ - Get just condensed number
    """
    
    queryset = NumberProperty.objects.all()
    serializer_class = NumberPropertySerializer
    lookup_field = 'number'
    
    def get_serializer_class(self):
        """Use simple serializer for list view."""
        if self.action == 'list':
            return NumberPropertySimpleSerializer
        return NumberPropertySerializer
    
    @action(detail=True, methods=['get'])
    def condensed(self, request, number=None):
        """
        Get just the condensed number for a day.
        
        GET /api/number-properties/14/condensed/
        
        Returns: {"number": 14, "condensed_number": 5}
        """
        try:
            day = int(number)
            condensed = NumberProperty.get_condensed_number(day)
            
            return Response({
                'number': day,
                'condensed_number': condensed
            })
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except NumberProperty.DoesNotExist as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'])
    def all_condensed(self, request):
        """
        Get all condensed numbers for days 1-31.
        
        GET /api/number-properties/all-condensed/
        
        Returns: {1: 1, 2: 2, 3: 3, ..., 14: 5, ..., 31: 4}
        """
        all_props = NumberProperty.objects.all().order_by('number')
        
        condensed_map = {
            prop.number: prop.condensed_number
            for prop in all_props
        }
        
        return Response({
            'count': len(condensed_map),
            'condensed_numbers': condensed_map
        })
