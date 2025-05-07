from django.shortcuts import render, redirect
from .models import Obras, InsumoUsado
from .forms import ObraForm, InsumoUsadoForm
from django.http import JsonResponse

def home(request):
    print("Renderizando home.html")
    obras = Obras.objects.all()
    return render(request, 'core/home.html', {'obras': obras})

def nova_obra(request):
    if request.method == 'POST':
        form = ObraForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = ObraForm()
    return render(request, 'core/nova_obra.html', {'form': form})

def novo_insumo(request):
    if request.method == 'POST':
        form = InsumoUsadoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = InsumoUsadoForm()
    return render(request, 'core/novo_insumo.html', {'form': form})

def ping(request):
    return JsonResponse({'message': 'pong from Django 🐍'})