from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ObraViewSet

router = DefaultRouter()
router.register(r'obras', ObraViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
