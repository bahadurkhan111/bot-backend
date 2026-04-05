from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from datetime import datetime
from .models import DateNumerology
from .serializers import DateNumerologySerializer, DateNumerologyCalculateSerializer
from .calculator import DateCalculator


class DateNumerologyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for Date Numerology calculations.
    
    Endpoints:
        GET /api/date-calculator/ - List cached numerologies
        GET /api/date-calculator/{date}/ - Get numerologies for specific date
        POST /api/date-calculator/calculate/ - Calculate numerologies for a date
    """
    
    queryset = DateNumerology.objects.all()
    serializer_class = DateNumerologySerializer
    lookup_field = 'date'
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        Calculate numerologies for a given date.
        
        POST /api/date-calculator/calculate/
        Body: {"date": "2026-01-14"}
        
        Returns all 13 numerologies with descriptions.
        """
        serializer = DateNumerologyCalculateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        date = serializer.validated_data['date']
        
        # Get or calculate numerologies
        numerology = DateNumerology.get_or_calculate(date)
        
        # Serialize response
        response_serializer = DateNumerologySerializer(numerology)
        
        return Response(response_serializer.data)
    
    @action(detail=False, methods=['get'])
    def today(self, request):
        """
        Get numerologies for today's date.
        
        GET /api/date-calculator/today/
        """
        from datetime import date
        today = date.today()
        
        numerology = DateNumerology.get_or_calculate(today)
        serializer = DateNumerologySerializer(numerology)
        
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def descriptions(self, request):
        """
        Get descriptions for all 13 numerologies.
        
        GET /api/date-calculator/descriptions/
        """
        descriptions = DateCalculator.get_numerology_descriptions()
        
        return Response({
            'numerologies': descriptions,
            'count': len(descriptions)
        })


@api_view(['GET'])
def quick_calculate(request):
    """
    Quick calculation endpoint.
    
    GET /api/date-calculator/quick/?date=2026-01-14
    
    Returns simplified numerology calculation.
    """
    date_str = request.query_params.get('date')
    
    if not date_str:
        return Response(
            {'error': 'Date parameter is required (format: YYYY-MM-DD)'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return Response(
            {'error': 'Invalid date format. Use YYYY-MM-DD'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Calculate numerologies
    calculator = DateCalculator()
    numerologies = calculator.calculate_all(date)
    
    return Response({
        'date': date_str,
        'numerologies': numerologies,
        'numerologies_list': list(numerologies.values())
    })
