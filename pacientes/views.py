from django.shortcuts import render, redirect
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