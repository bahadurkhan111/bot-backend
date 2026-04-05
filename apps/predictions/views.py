"""
API Views for predictions.
"""
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes as perm_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .models import Team, Game, Prediction
from .serializers import (
    TeamSerializer,
    GameSerializer,
    PredictionSerializer,
    PredictionRequestSerializer,
    PredictionResponseSerializer,
    PredictionStatsSerializer,
    PredictionCalculateSerializer,
    PredictionCalculateResponseSerializer,
    PredictionAutoCalculateSerializer,
)
from .services import PredictionService
from .formula import apply_formula
from .pattern_recognition import pattern_tracker
from apps.calculators.registry import CalculatorRegistry

logger = logging.getLogger(__name__)


@api_view(['GET'])
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({"status": "healthy", "service": "sportbot-backend"})


class TeamViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing teams.
    """
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['sport']
    search_fields = ['name']


class GameViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for viewing games.
    """
    queryset = Game.objects.select_related('team1', 'team2', 'actual_winner').all()
    serializer_class = GameSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['status', 'date']
    search_fields = ['team1__name', 'team2__name']


class PredictionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet for predictions with custom actions.
    """
    queryset = Prediction.objects.select_related(
        'game',
        'game__team1',
        'game__team2',
        'predicted_winner'
    ).all()
    serializer_class = PredictionSerializer
    permission_classes = [AllowAny]
    filterset_fields = ['signal', 'was_correct']
    ordering_fields = ['created_at', 'confidence', 'model_consensus']
    ordering = ['-created_at']
    
    @action(detail=False, methods=['post'])
    def predict(self, request):
        """
        Create a new prediction.
        
        POST /api/predictions/predict/
        Request: {"team1": "Lakers", "team2": "Celtics", "sport": "NBA"}
        """
        serializer = PredictionRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team1 = serializer.validated_data['team1']
        team2 = serializer.validated_data['team2']
        sport = serializer.validated_data.get('sport', 'NBA')
        
        logger.info(f"Prediction request: {team1} vs {team2} ({sport})")
        
        # Create prediction
        result = PredictionService.create_prediction(team1, team2, sport)
        
        if result is None:
            return Response(
                {'error': 'Failed to create prediction. Please check model files.'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        prediction, response_data = result
        
        return Response(
            response_data,
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'])
    def history(self, request):
        """
        Get prediction history.
        
        GET /api/predictions/history/
        """
        queryset = self.filter_queryset(self.get_queryset())[:20]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    @method_decorator(cache_page(60 * 5))  # Cache for 5 minutes
    def stats(self, request):
        """
        Get prediction statistics.
        
        GET /api/predictions/stats/
        """
        stats = PredictionService.get_prediction_stats()
        serializer = PredictionStatsSerializer(stats)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def recent(self, request):
        """
        Get recent predictions (last 10).
        
        GET /api/predictions/recent/
        """
        queryset = self.get_queryset()[:10]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        Calculate prediction using the formula directly.
        
        POST /api/predictions/calculate/
        Request: {
            "linear_output": 6.32,
            "day_of_month": 14,
            "game_date": "2026-01-14",  # Optional
            "sport": "NBA"
        }
        
        Response: {
            "linear_output": 6.32,
            "day_of_month": 14,
            "base_number": 4,
            "base_calculation": "...",
            "properties": [...],
            "date_digit_sum": 16,
            "game_date": "2026-01-14",
            "step_1_sum": 26.32,
            "step_2_divide": 13.16,
            "step_3_multiply": 52.64,
            "sport": "NBA",
            "sport_multiplier": 1.15,
            "predicted_total": 52.64,
            "formula_steps": [...],
            "formula_latex": "..."
        }
        """
        serializer = PredictionCalculateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        linear_output = serializer.validated_data['linear_output']
        day_of_month = serializer.validated_data['day_of_month']
        game_date = serializer.validated_data.get('game_date')
        sport = serializer.validated_data.get('sport', 'NBA')
        
        logger.info(f"Formula calculation: L={linear_output}, day={day_of_month}, date={game_date}, sport={sport}")
        
        try:
            result = apply_formula(
                linear_output=linear_output,
                day_of_month=day_of_month,
                game_date=game_date,
                sport=sport
            )
            # Auto-save to pattern tracker so it shows in Patterns tab
            try:
                pattern_tracker.log_prediction(
                    sport=sport,
                    day=day_of_month,
                    predicted_total=result['predicted_total'],
                    linear_output=linear_output,
                    base_number=result.get('base_number', 0),
                    date_digit_sum=result.get('date_digit_sum', 0),
                    game_date=result.get('game_date'),
                )
                result['prediction_id'] = len(pattern_tracker.predictions)
            except Exception as pe:
                logger.error(f"Pattern log error: {pe}")
            return Response(result, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Formula calculation error: {str(e)}")
            return Response(
                {'error': f'Calculation failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=False, methods=['post'])
    def predict_auto(self, request):
        """
        Calculate prediction automatically with ML model for team matchup.
        
        POST /api/predictions/predict_auto/
        Request: {
            "team1": "Lakers",
            "team2": "Celtics",
            "day_of_month": 14,
            "sport": "NBA"
        }
        
        Response: {
            "team1": "Lakers",
            "team2": "Celtics",
            "linear_output": 6.32,
            "day_of_month": 14,
            "condensed_number": 5,
            "truest_number": 9,
            "sport": "NBA",
            "sport_multiplier": 1.15,
            "predicted_total": 10.35,
            "predicted_winner": "Lakers",
            "confidence": 75.5,
            "model_breakdown": {...},
            "formula_steps": [...]
        }
        """
        serializer = PredictionAutoCalculateSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        
        team1 = serializer.validated_data['team1']
        team2 = serializer.validated_data['team2']
        day_of_month = serializer.validated_data['day_of_month']
        sport = serializer.validated_data.get('sport', 'NBA')
        
        logger.info(f"Auto prediction: {team1} vs {team2}, day={day_of_month}, sport={sport}")
        
        try:
            # Get ML prediction
            result = PredictionService.create_prediction(team1, team2, sport)
            
            if result is None:
                return Response(
                    {'error': 'Failed to create prediction. Model may not be loaded.'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            prediction, prediction_data = result
            
            # Get linear regression output from the prediction
            linear_output = prediction.linear_prediction
            
            # Apply formula with the linear output
            formula_result = apply_formula(
                linear_output=linear_output,
                day_of_month=day_of_month,
                sport=sport
            )
            
            # Combine results
            combined_result = {
                'team1': team1,
                'team2': team2,
                'predicted_winner': prediction_data['predicted_winner'],
                'confidence': prediction_data['confidence'],
                'signal': prediction_data['signal'],
                'model_consensus': prediction_data['model_consensus'],
                'model_breakdown': prediction_data['model_breakdown'],
                'recommendation': prediction_data['recommendation'],
                **formula_result  # Add all formula results
            }
            
            return Response(combined_result, status=status.HTTP_200_OK)
            
        except Exception as e:
            logger.error(f"Auto prediction error: {str(e)}", exc_info=True)
            return Response(
                {'error': f'Prediction failed: {str(e)}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CalculatorViewSet(viewsets.ViewSet):
    """
    ViewSet for gematria calculators.
    """
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['get'])
    def list_calculators(self, request):
        """
        List all available calculators.
        
        GET /api/calculators/list/
        """
        info = CalculatorRegistry.get_calculator_info()
        return Response(info)
    
    @action(detail=False, methods=['post'])
    def calculate(self, request):
        """
        Calculate gematria values for text.
        
        POST /api/calculators/calculate/
        Request: {"text": "Lakers"}
        """
        text = request.data.get('text')
        
        if not text:
            return Response(
                {'error': 'Text parameter is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        results = CalculatorRegistry.calculate_all(text)
        
        return Response({
            'text': text,
            'values': results
        })
    
    @action(detail=False, methods=['post'])
    def calculate_specific(self, request):
        """
        Calculate using a specific calculator.
        
        POST /api/calculators/calculate_specific/
        Request: {"text": "Lakers", "calculator": "ordinal"}
        """
        text = request.data.get('text')
        calculator_name = request.data.get('calculator')
        
        if not text or not calculator_name:
            return Response(
                {'error': 'Both text and calculator parameters are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        calculator = CalculatorRegistry.get_calculator(calculator_name)
        
        if calculator is None:
            return Response(
                {'error': f'Calculator "{calculator_name}" not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        value = calculator.calculate(text)

        return Response({
            'text': text,
            'calculator': calculator_name,
            'value': value
        })


# ============================================================
# Pattern Recognition & Loss-Aware Adjustment Endpoints
# ============================================================

@api_view(['GET'])
@perm_classes([AllowAny])
def patterns_view(request):
    """
    Get detected patterns from prediction history.

    GET /api/patterns/
    """
    summary = pattern_tracker.get_patterns_summary()
    return Response(summary)


@api_view(['GET'])
@perm_classes([AllowAny])
def accuracy_view(request):
    """
    Get prediction accuracy statistics.

    GET /api/accuracy/
    """
    stats = pattern_tracker.get_accuracy_stats()
    return Response(stats)


@api_view(['POST'])
@perm_classes([AllowAny])
def record_outcome_view(request):
    """
    Record actual outcome for a prediction.

    POST /api/outcomes/
    Request: {"prediction_id": 1, "actual_total": 215.5}
    """
    prediction_id = request.data.get('prediction_id')
    actual_total = request.data.get('actual_total')

    if prediction_id is None or actual_total is None:
        return Response(
            {'error': 'prediction_id and actual_total are required'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        prediction_id = int(prediction_id)
        actual_total = float(actual_total)
    except (ValueError, TypeError):
        return Response(
            {'error': 'Invalid prediction_id or actual_total'},
            status=status.HTTP_400_BAD_REQUEST
        )

    success = pattern_tracker.record_outcome(prediction_id, actual_total)

    if success:
        return Response({
            'success': True,
            'adjustment_factor': pattern_tracker.adjustment_factor,
            'message': f'Outcome recorded for prediction #{prediction_id}'
        })
    else:
        return Response(
            {'error': f'Prediction #{prediction_id} not found'},
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
@perm_classes([AllowAny])
def prediction_log_view(request):
    """
    Get prediction log history.

    GET /api/prediction-log/
    """
    limit = int(request.query_params.get('limit', 50))
    predictions = pattern_tracker.predictions[-limit:]
    return Response({
        'predictions': list(reversed(predictions)),
        'total': len(pattern_tracker.predictions),
        'adjustment_factor': pattern_tracker.adjustment_factor,
    })


# ============================================================
# Sports Data Scraper Endpoints
# ============================================================

@api_view(['GET'])
@perm_classes([AllowAny])
def sports_scores_view(request):
    """
    Get sports scores for a date.

    GET /api/sports-data/scores/?sport=NBA&date=2026-03-19
    """
    try:
        from .sports_scraper import sports_scraper

        sport = request.query_params.get('sport', 'NBA')
        date_str = request.query_params.get('date')

        games = sports_scraper.get_scores(sport, date_str)
        return Response({
            'sport': sport,
            'date': date_str,
            'games': games,
        })
    except ImportError:
        return Response({
            'error': 'Sports scraper requires beautifulsoup4. Install with: pip install beautifulsoup4',
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
    except Exception as e:
        logger.error(f"Sports scores error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@perm_classes([AllowAny])
def sports_standings_view(request):
    """
    Get current standings.

    GET /api/sports-data/standings/?sport=NBA
    """
    try:
        from .sports_scraper import sports_scraper

        sport = request.query_params.get('sport', 'NBA')
        standings = sports_scraper.get_standings(sport)

        if standings:
            return Response(standings)
        else:
            return Response({'error': 'Could not fetch standings'}, status=status.HTTP_404_NOT_FOUND)
    except ImportError:
        return Response({
            'error': 'Sports scraper requires beautifulsoup4.',
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
    except Exception as e:
        logger.error(f"Standings error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@perm_classes([AllowAny])
def team_stats_view(request):
    """
    Get team statistics from reference sites.

    GET /api/sports-data/team/?sport=NBA&team=Lakers
    """
    try:
        from .sports_scraper import sports_scraper

        sport = request.query_params.get('sport', 'NBA')
        team = request.query_params.get('team', '')

        if not team:
            return Response({'error': 'team parameter required'}, status=status.HTTP_400_BAD_REQUEST)

        stats = sports_scraper.get_team_stats(sport, team)

        if stats:
            return Response(stats)
        else:
            return Response({'error': f'No stats found for {team}'}, status=status.HTTP_404_NOT_FOUND)
    except ImportError:
        return Response({
            'error': 'Sports scraper requires beautifulsoup4.',
        }, status=status.HTTP_501_NOT_IMPLEMENTED)
    except Exception as e:
        logger.error(f"Team stats error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================
# News Headlines + Gematria Pipeline Endpoints
# ============================================================

@api_view(['GET'])
@perm_classes([AllowAny])
def news_headlines_view(request):
    """
    Get news headlines with gematria analysis.

    GET /api/news/headlines/?source=CNN&limit=10
    """
    try:
        from .news_scraper import news_scraper

        source = request.query_params.get('source', 'CNN').upper()
        limit = int(request.query_params.get('limit', 10))

        analysis = news_scraper.analyze_headlines(source, limit)
        return Response(analysis)
    except Exception as e:
        logger.error(f"News headlines error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@perm_classes([AllowAny])
def news_combined_view(request):
    """
    Get combined news analysis from all sources.

    GET /api/news/combined/?limit=10
    """
    try:
        from .news_scraper import news_scraper

        limit = int(request.query_params.get('limit', 10))
        result = news_scraper.get_combined_analysis(limit)
        return Response(result)
    except Exception as e:
        logger.error(f"Combined news error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ============================================================
# Coaches Data Endpoint
# ============================================================

@api_view(['POST'])
@perm_classes([AllowAny])
def unified_predict_view(request):
    """
    Unified prediction endpoint — runs everything in one call:
    ML prediction + formula + gematria breakdown + live scores + news signals + auto-saves pattern.

    POST /api/predict/
    Request: {"team1": "Lakers", "team2": "Rockets", "sport": "NBA", "day_of_month": 19, "game_date": "2026-03-19"}
    """
    team1_name = request.data.get('team1', '')
    team2_name = request.data.get('team2', '')
    sport = request.data.get('sport', 'NBA')
    day_of_month = request.data.get('day_of_month')
    game_date = request.data.get('game_date')

    if not team1_name or not team2_name:
        return Response({'error': 'team1 and team2 are required'}, status=status.HTTP_400_BAD_REQUEST)

    from datetime import datetime

    if not day_of_month:
        day_of_month = datetime.now().day
    else:
        day_of_month = int(day_of_month)

    if not game_date:
        game_date = datetime.now().strftime('%Y-%m-%d')

    result = {}

    # 1. ML Prediction
    ml_data = None
    linear_output = 6.32  # default
    try:
        ml_result = PredictionService.create_prediction(team1_name, team2_name, sport)
        if ml_result:
            prediction_obj, ml_data = ml_result
            linear_output = prediction_obj.linear_prediction or 6.32
            result['ml_prediction'] = ml_data
    except Exception as e:
        logger.error(f"ML prediction error: {e}")
        result['ml_prediction'] = None

    # 2. Formula Calculation
    try:
        formula_result = apply_formula(
            linear_output=linear_output,
            day_of_month=day_of_month,
            game_date=game_date,
            sport=sport
        )
        result['formula'] = formula_result
    except Exception as e:
        logger.error(f"Formula error: {e}")
        result['formula'] = None

    # 3. Gematria Breakdown for both teams
    try:
        gematria_values = {}
        from apps.calculators.registry import CalculatorRegistry
        gematria_values['team1'] = {
            'name': team1_name,
            'values': CalculatorRegistry.calculate_all(team1_name)
        }
        gematria_values['team2'] = {
            'name': team2_name,
            'values': CalculatorRegistry.calculate_all(team2_name)
        }
        result['gematria'] = gematria_values
    except Exception as e:
        logger.error(f"Gematria error: {e}")
        result['gematria'] = None

    # 4. Live Scores
    try:
        from .sports_scraper import sports_scraper
        scores = sports_scraper.get_scores(sport)
        t1 = team1_name.lower()
        t2 = team2_name.lower()
        matching = [g for g in scores if
                    t1 in g['team1'].lower() or t1 in g['team2'].lower() or
                    t2 in g['team1'].lower() or t2 in g['team2'].lower()]
        result['live_scores'] = matching if matching else scores[:5]
    except Exception as e:
        logger.error(f"Scores error: {e}")
        result['live_scores'] = []

    # 5. News Gematria Signals
    try:
        from .news_scraper import news_scraper
        news = news_scraper.analyze_headlines('CNN', 5)
        result['news_signals'] = {
            'key_numbers': news.get('key_numbers', {}),
            'headline_count': news.get('headline_count', 0),
            'top_headlines': [h['title'] for h in news.get('headlines', [])[:3]],
        }
    except Exception as e:
        logger.error(f"News error: {e}")
        result['news_signals'] = None

    # 6. Auto-save to pattern tracker
    try:
        if result.get('formula') and result['formula'].get('predicted_total'):
            pattern_tracker.log_prediction({
                'team1': team1_name,
                'team2': team2_name,
                'sport': sport,
                'predicted_total': result['formula']['predicted_total'],
                'day_of_month': day_of_month,
                'base_number': result['formula'].get('base_number'),
                'linear_output': linear_output,
            })
            result['pattern_saved'] = True
    except Exception as e:
        logger.debug(f"Pattern save error: {e}")
        result['pattern_saved'] = False

    # 7. Pattern stats
    try:
        result['pattern_stats'] = pattern_tracker.get_accuracy_stats()
    except Exception:
        result['pattern_stats'] = None

    result['team1'] = team1_name
    result['team2'] = team2_name
    result['sport'] = sport

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
@perm_classes([AllowAny])
def coaches_view(request):
    """
    Get coaches/managers for a sport.

    GET /api/sports-data/coaches/?sport=NBA
    """
    try:
        from .sports_scraper import sports_scraper

        sport = request.query_params.get('sport', 'NBA')
        coaches = sports_scraper.get_coaches(sport)

        if coaches:
            return Response({
                'sport': sport.upper(),
                'coaches': coaches,
            })
        else:
            return Response({'error': f'No coaches data found for {sport}'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Coaches error: {e}")
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
