from django.urls import path
from .api_views import criar_obra, ping

urlpatterns = [
    path('ping/', ping),
    path('obras/', criar_obra),
]
