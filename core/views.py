from django.shortcuts import render
from .models import Obras

def home(request):
    print("Renderizando home.html")
    obras = Obras.objects.all()
    return render(request, 'core/home.html', {'obras': obras})
