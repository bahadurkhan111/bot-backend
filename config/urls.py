"""
URL configuration for sports-prediction-bot project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.predictions.urls')),
    path('api/bot/', include('apps.bot.urls')),
    path('api/date-calculator/', include('apps.date_calculator.urls')),
    path('api/number-properties/', include('apps.number_properties.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
