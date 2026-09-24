import requests
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Paciente

def menu_vitrine(request):
    return render (request, 'index.html')

def menu_painel(request):
    return render (request, 'menu2.html')

def login_view(request):

    if request.method == "POST":
        email_digitado = request.POST.get('email')
        senha_digitada = request.POST.get('senha')

        try:
            paciente = Paciente.objects.get(email=email_digitado, senha=senha_digitada)

            request.session['paciente_id'] = paciente.id

            return redirect('home_privada')
    
        except Paciente.DoesNotExist:
            erro = "Email ou senha incorretos. Tente novamente!"

    return render(request, 'login.html')

def cadastro_view(request):
    if request.method == "POST":
        nome_digitado = request.POST.get('nome')
        cpf_digitado = request.POST.get('cpf')
        email_digitado = request.POST.get('email')
        senha_digitado = request.POST.get('senha')

        Paciente.objects.create(
            nome=nome_digitado,
            cpf=cpf_digitado,
            email=email_digitado,
            senha=senha_digitado            
        )

        return redirect('home_privada')

    return render(request, 'cadastro.html')

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

def perfil_view(request):
    return render (request, 'pagina_usuario.html') 