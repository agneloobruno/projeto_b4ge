from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import Obras
from .serializers import ObrasSerializer

@api_view(['POST'])
def criar_obra(request):
    serializer = ObrasSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def ping(request):
    return Response({"message": "pong from Django 🔁"})
