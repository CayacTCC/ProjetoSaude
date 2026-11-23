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
        # Se veio hospital_id na URL, usa ele; se não, pega o que o usuário escolheu no form
        id_escolhido = hospital_id or request.POST.get('hospital_id')
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
        return redirect('fantasma_consulta')

    return render(request, 'FantasmaDoAgendar.html', {
        'hospital': hospital_fixo,
        'hospitais': hospitais,
    })