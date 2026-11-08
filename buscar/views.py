from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from hospital.models import Hospital, PlanoSaude, Exame, ExameEspecifico
from pacientes.models import Paciente
from pacientes import views
from pacientes.models import Paciente
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

@login_required(login_url='pagina_login')
def buscar_hospitais(request):
    cidade_escolhida = request.GET.get('cidade', '').strip()
    plano_id = request.GET.get('plano', '').strip()
    exame_id = request.GET.get('exame','').strip()
    perto = request.GET.get('perto_de_mim') == 'on'

    hospitais = Hospital.objects.all()

    if cidade_escolhida:
        hospitais = hospitais.filter(cidade__icontains=cidade_escolhida)

    if plano_id:
        hospitais = hospitais.filter(planos_aceitos__id=plano_id)

    if exame_id:
        hospitais = hospitais.filter(exame_disponiveis__id=exame_id)

    ordem = []
    paciente = Paciente.objects.filter(usuario=request.user).first()

    if perto and paciente and paciente.rua:
        geolocator = Nominatim(user_agent="app_saude_baixada_santista")
        endereco_busca = f"{paciente.rua}, {paciente.cidade or  'Santos'}, SP, Brasil"
        local_paciente = geolocator.geocode(endereco_busca)

        if local_paciente:
            ponto_paciente = (local_paciente.latitude, local_paciente.longitude)

            for hospital in hospitais:
                if hospital.latitude and hospital.longitude:
                    ponto_hospital = (hospital.latitude, hospital.longitude)
                    distancia = geodesic(ponto_paciente, ponto_hospital).km
                    ordem.append({
                        'hospital': hospital,
                        'distancia_km': round(distancia, 1)
                    })

            ordem.sort(key=lambda item: item ['distancia_km'])

    else:
        for hospital in hospitais:
            ordem.append({
                'hospital': hospital,
                'distancia_km': None
            })

    context = {
        'hospitais_distante': ordem,
        'planos': PlanoSaude.objects.all,
        'exames': ExameEspecifico.objects.all,
        'municipios_baixada': ['Santos', 'São Vicente', 'Praia Grande', 'Cubatão', 'Guarujá', 'Itanhaém', 'Bertioga', 'Mongaguá', 'Peruíbe']
    }

    return render(request, 'busca.html', context)