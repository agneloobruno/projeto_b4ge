# b4ge_calculadora/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/', include('core.urls')),  # ✅ removido 'api/'
    path('admin/', admin.site.urls),
]
