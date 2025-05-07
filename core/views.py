from django.shortcuts import render
from .models import Obras
from .forms import ObraForm

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