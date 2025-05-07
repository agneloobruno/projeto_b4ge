from core.views import home
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
