from django.http import JsonResponse
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
    exames = ExameEspecifico.objects.all()

    cidades = (
        Hospital.objects.exclude(cidade__isnull=True)
        .exclude(cidade__exact='')
        .values_list('cidade', flat=True)
        .distinct()
        .order_by('cidade')
    )

    hospital_fixo = None
    if hospital_id is not None:
        hospital_fixo = get_object_or_404(Hospital, id=hospital_id)

    if request.method == "POST":
        id_escolhido = hospital_id or request.POST.get('hospital_id')
        if not id_escolhido:
            messages.error(request, "Selecione um hospital antes de confirmar o agendamento.")
            return render(request, 'agendamento.html', {
                'hospital': hospital_fixo,
                'hospitais': hospitais,
                'exames': exames,
                'cidades': cidades,
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
        'exames': exames,
        'cidades': cidades,
    })


@login_required(login_url='pagina_login')
def api_hospitais_por_cidade(request):
    cidade = request.GET.get('cidade', '').strip()
    tipo = request.GET.get('tipo_atendimento', '').strip().upper()
    paciente = get_object_or_404(Paciente, usuario=request.user)

    hospitais = Hospital.objects.filter(cidade__iexact=cidade)

    if tipo == 'PLANO':
        if paciente.plano_de_saude:
            hospitais = hospitais.filter(planos_aceitos=paciente.plano_de_saude)
        else:
            hospitais = Hospital.objects.none()

    hospitais = hospitais.order_by('nome').distinct()

    return JsonResponse({
        'hospitais': [{'id': h.id, 'nome': h.nome} for h in hospitais]
    })


@login_required(login_url='pagina_login')
def api_exames_por_hospital(request, hospital_id):
    hospital = get_object_or_404(Hospital, id=hospital_id)
    exames = hospital.exames_disponiveis.all().order_by('nome')

    return JsonResponse({
        'exames': [
            {
                'id': e.id,
                'nome': e.nome,
                'descricao': e.descricao or '',
            }
            for e in exames
        ]
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