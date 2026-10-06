from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agendamento
from pacientes.models import Paciente
from hospital.models import Hospital, ExameEspecifico

@login_required(login_url='pagina_login')
def criar_agendamento(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    paciente = get_object_or_404(Paciente, usuario=request.user)

    if request.method == "POST":
        exame_id = request.POST.get('exame_id')
        data = request.POST.get('data')
        horario = request.POST.get('horario')
        obs = request.POST.get('observacoes')

        exame = ExameEspecifico.objects.filter(id=exame_id).first() if exame_id else None

        Agendamento.objects.create(
            paciente=paciente,
            hospital=hospital,
            exame_especifico=exame,
            data_consulta=data,
            horario_consulta=horario,
            observacoes=obs
        )
        messages.success(request, "Consulta agendada com sucesso!")
        return redirect('fantasma_consulta')

    return render(request, 'FantasmaDoAgendar.html', {'hospital': hospital})

@login_required(login_url='pagina_login')
def minhas_consultas(request):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    consultas = Agendamento.objects.filter(paciente=paciente)
    return render (request, 'FantasmaDoMinhasConsultas.html', {'consultas': consultas})

@login_required(login_url='pagina_login')
def cancelar_agendamento(request, agendamento_id):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, paciente=paciente)

    if request.method == "POST":
        agendamento.status = 'CANCELADO'
        agendamento.save()
        messages.success(request, "Agendamento cancelado com sucesso!")

    return redirect('minhas_consultas')