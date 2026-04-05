"""
URL configuration for predictions API.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TeamViewSet, GameViewSet, PredictionViewSet, CalculatorViewSet, health_check,
    patterns_view, accuracy_view, record_outcome_view, prediction_log_view,
    sports_scores_view, sports_standings_view, team_stats_view,
    news_headlines_view, news_combined_view, coaches_view,
    unified_predict_view,
)

router = DefaultRouter()
router.register(r'teams', TeamViewSet, basename='team')
router.register(r'games', GameViewSet, basename='game')
router.register(r'predictions', PredictionViewSet, basename='prediction')
router.register(r'calculators', CalculatorViewSet, basename='calculator')

urlpatterns = [
    path('health/', health_check, name='health_check'),
    path('predict/', unified_predict_view, name='unified_predict'),

    # Pattern recognition & loss-aware adjustment
    path('patterns/', patterns_view, name='patterns'),
    path('accuracy/', accuracy_view, name='accuracy'),
    path('outcomes/', record_outcome_view, name='record_outcome'),
    path('prediction-log/', prediction_log_view, name='prediction_log'),

    # Sports data scraper
    path('sports-data/scores/', sports_scores_view, name='sports_scores'),
    path('sports-data/standings/', sports_standings_view, name='sports_standings'),
    path('sports-data/team/', team_stats_view, name='team_stats'),
    path('sports-data/coaches/', coaches_view, name='coaches'),

    # News headlines + gematria pipeline
    path('news/headlines/', news_headlines_view, name='news_headlines'),
    path('news/combined/', news_combined_view, name='news_combined'),

    path('', include(router.urls)),
]
