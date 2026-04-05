from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'', views.DateNumerologyViewSet, basename='date-numerology')

urlpatterns = [
    path('quick/', views.quick_calculate, name='quick-calculate'),
    path('', include(router.urls)),
]
