#já arrumado

import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Paciente
from hospital.models import PlanoSaude

def menu_vitrine(request):
    return render (request, 'index.html')

@login_required(login_url='pagina_login')
def menu_painel(request):
    return render (request, 'menu2.html')

def login_view(request):
    if request.method == "POST":
        email_digitado = request.POST.get('email')
        senha_digitada = request.POST.get('senha')

        try:
            user = User.objects.get(email=email_digitado)
            user_autenticado = authenticate(request, username=user.username, password=senha_digitada)

            if user_autenticado is not None:
                login(request, user_autenticado)
                return redirect('home_privada')
            else :
                messages.error(request, "Senha incorreta. Tente novamente!")

        except User.DoesNotExist:
            messages.error(request, "Email não encontrado.")
    
    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == "POST":
        nome_digitado = request.POST.get('nome')
        cpf_digitado = request.POST.get('cpf')
        email_digitado = request.POST.get('email')
        senha_digitada = request.POST.get('senha')

        if User.objects.filter(email=email_digitado).exists():
            messages.error(request, "Este email já está cadastrado.")
            return render(request, 'cadastro.html')

        user = User.objects.create_user(
            username=email_digitado,
            email=email_digitado,
            password=senha_digitada,
            first_name=nome_digitado
        )

        Paciente.objects.create(
            usuario=user,
            cpf=cpf_digitado            
        )

        login(request, user)
        return redirect('home_privada')

    return render(request, 'cadastro.html')

@login_required(login_url='pagina_login')
def cadastro_enderecoP(request):
    if request.method == "POST":
        cep_digitado = request.POST.get('cep', '').replace('-', '').strip()

        if cep_digitado:
            url = f"https://viacep.com.br/ws/{cep_digitado}/json/"
        
            try:
                resposta = requests.get(url)

                if resposta.status_code == 200:
                    dados = resposta.json()

                    if "erro" not in dados:
                        try:
                            perfil = Paciente.objects.get(usuario=request.user)

                            perfil.cep = cep_digitado
                            perfil.rua = dados.get('logradouro')
                            perfil.bairro = dados.get('bairro')
                            perfil.cidade = dados.get('localidade')
                            perfil.uf = dados.get('uf')

                            perfil.save()
                            messages.success(request, "Endereço atualizado com sucesso!")
                            return redirect('perfil_usuario')

                        except Paciente.DoesNotExist:
                            messages.error(request, "Perfil de paciente não encontrado.")
        
                    else:
                        messages.error(request, "CEP não encontrado.")
            except requests.exceptions.RequestException:
                messages.error(request, "Erro ao consultar o ViaCEP. Tente novamente.")

    return render(request, 'pagina_usuario.html')

TIPOS_SANGUINEOS = ['AB+', 'AB-', 'A+', 'A-', 'B+', 'B-', 'O+', 'O-']


@login_required(login_url='pagina_login')
def perfil_view(request):
    paciente, _ = Paciente.objects.get_or_create(
        usuario=request.user,
        defaults={'cpf': ''}
    )
    planos_saude = PlanoSaude.objects.all()

    if request.method == "POST":
        acao = request.POST.get('acao', '')

        if acao == 'atualizar_prontuario':
            tipo_sang = request.POST.get('tipo_sanguineo', '').strip()
            doencas = request.POST.get('doencas_cronicas', '').strip()
            plano_id = request.POST.get('plano_de_saude')

            paciente.tipo_sanguineo = tipo_sang if tipo_sang in TIPOS_SANGUINEOS else None
            paciente.doencas_cronicas = doencas or None
            paciente.plano_de_saude = (
                PlanoSaude.objects.filter(id=plano_id).first() if plano_id else None
            )
            paciente.save()

            messages.success(request, "Dados do prontuário atualizados com sucesso!")
            return redirect('perfil_usuario')

        cep_digitado = request.POST.get('cep', '').replace('-', '').strip()
        rua_digitada = request.POST.get('rua', '').strip()
        bairro_digitada = request.POST.get('bairro', '').strip()
        cidade_digitada = request.POST.get('cidade', '').strip()
        uf_digitada = request.POST.get('uf', '').strip().upper()

        paciente.cep = cep_digitado
        paciente.rua = rua_digitada
        paciente.bairro = bairro_digitada
        paciente.cidade = cidade_digitada
        paciente.uf = uf_digitada
        paciente.save()

        messages.success(request, "Endereço atualizado com sucesso!")
        return redirect('perfil_usuario')

    return render(request, 'pagina_usuario.html', {
        'paciente': paciente,
        'planos_saude': planos_saude,
        'tipos_sanguineos': TIPOS_SANGUINEOS,
    })