from django.shortcuts import render, redirect
from .models import Obras, InsumoUsado
from .forms import ObraForm, InsumoUsadoForm
from django.http import JsonResponse
from .serializers import ObrasSerializer
from rest_framework import viewsets

def home(request):
    obras = Obras.objects.all()
    return render(request, 'core/home.html', {'obras': obras})

def nova_obra(request):
    form = ObraForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'core/nova_obra.html', {'form': form})

def novo_insumo(request):
    form = InsumoUsadoForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('home')
    return render(request, 'core/novo_insumo.html', {'form': form})

def ping(request):
    return JsonResponse({'message': 'pong from Django 🔁'})

class ObraViewSet(viewsets.ModelViewSet):
    queryset = Obras.objects.all()
    serializer_class = ObrasSerializer
