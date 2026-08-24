from django.shortcuts import render, redirect
from .models import Paciente

def menu_vitrine(request):
    return render (request, 'index.html')

def menu_painel(request):
    return render (request, 'index.html')

def login_view(request):
    return render (request, 'login.html')

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

        return redirect('login')

    return render(request, 'cadastro.html')