from django.shortcuts import render, redirect, get_object_or_404
from .models import Evento
from .forms import EventoForm
from django.contrib.auth.decorators import login_required

@login_required
def pagina_inicial(request):
    eventos = Evento.objects.filter(data_inicio__gte=timezone.now()).order_by('data_inicio')
    return render(request, 'pagina_inicial.html', {'eventos': eventos})

@login_required
def detalhe_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    return render(request, 'detalhe_evento.html', {'evento': evento})

@login_required
def criar_evento(request):
    if request.method == "POST":
        form = EventoForm(request.POST)
        if form.is_valid():
            evento = form.save(commit=False)
            evento.criador = request.user
            evento.save()
            return redirect('pagina_inicial')
    else:
        form = EventoForm()
    return render(request, 'criar_evento.html', {'form': form})

@login_required
def editar_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.user != evento.criador:
        return redirect('pagina_inicial')
    if request.method == "POST":
        form = EventoForm(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return redirect('detalhe_evento', evento_id=evento_id)
    else:
        form = EventoForm(instance=evento)
    return render(request, 'editar_evento.html', {'form': form})

@login_required
def excluir_evento(request, evento_id):
    evento = get_object_or_404(Evento, pk=evento_id)
    if request.user == evento.criador:
        evento.delete()
    return redirect('pagina_inicial')

