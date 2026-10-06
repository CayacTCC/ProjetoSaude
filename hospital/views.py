from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from .models import Hospital
from pacientes.models import Paciente

@login_required(login_url='pagina_login')
def listar_hospitais_perto(request):
    paciente = Paciente.objects.get(usuario=request.user)

    geolocator = Nominatim(user_agent="app_saude_baixada_santista")
    endereco_busca = f"{paciente.rua or ''}, {paciente.cidade or 'Santos'}, SP, Brasil"
    local_paciente = geolocator.geocode(endereco_busca)
    hospitais = Hospital.objects.all()
    lista_ordenada = []

    if local_paciente:
        ponto_paciente = (local_paciente.latitude, local_paciente.longitude)

        for hospital in hospitais:
            if hospital.latitude and hospital.longitude:
                ponto_hospital = (hospital.latitude, hospital.longitude)

                distancia = geodesic(ponto_paciente, ponto_hospital).km

                lista_ordenada.append({
                    'hospital': hospital,
                    'distancia_km': round(distancia, 1)
                })

        lista_ordenada.sort(key=lambda item: item['distancia_km'])

    return render(request, 'arquivo_fantasma.html', {
        'hospitais_com_distancia': lista_ordenada,
        'paciente': paciente
    })