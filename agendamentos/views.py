from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Agendamento
from pacientes.models import Paciente
from hospital.models import Hospital, ExameEspecifico


@login_required(login_url='pagina_login')
def criar_agendamento(request, hospital_id=None):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    hospitais = Hospital.objects.all()

    hospital_fixo = None
    if hospital_id is not None:
        hospital_fixo = get_object_or_404(Hospital, id=hospital_id)

    if request.method == "POST":
        id_escolhido = hospital_id or request.POST.get('hospital_id')
        if not id_escolhido:
            messages.error(request, "Selecione um hospital antes de agendar.")
            return render(request, 'agendamento.html', {
                'hospital': hospital_fixo,
                'hospitais': hospitais,
            })

        hospital = get_object_or_404(Hospital, id=id_escolhido)

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
        return redirect('minhas_consultas')

    return render(request, 'agendamento.html', {
        'hospital': hospital_fixo,
        'hospitais': hospitais,
    })


@login_required(login_url='pagina_login')
def minhas_consultas(request):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    consultas = Agendamento.objects.filter(paciente=paciente)
    return render(request, 'consultas.html', {'consultas': consultas})


@login_required(login_url='pagina_login')
def cancelar_agendamento(request, agendamento_id):
    paciente = get_object_or_404(Paciente, usuario=request.user)
    agendamento = get_object_or_404(Agendamento, id=agendamento_id, paciente=paciente)

    if request.method == "POST":
        agendamento.status = 'CANCELADO'
        agendamento.save()
        messages.success(request, "Agendamento cancelado com sucesso!")

    return redirect('minhas_consultas')