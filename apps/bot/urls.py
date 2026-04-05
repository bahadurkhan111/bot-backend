"""
URL Configuration for ChatBot API
"""
from django.urls import path
from .views import chatbot_message, chatbot_info

urlpatterns = [
    path('chat/', chatbot_message, name='chatbot-message'),
    path('info/', chatbot_info, name='chatbot-info'),
]
