from django.db import models
from django.contrib.auth.models import User
from hospital.models import PlanoSaude

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente_perfil')

    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    cep = models.CharField(max_length=9, blank=True, null=True)
    rua = models.CharField(max_length=150, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    plano_de_saude = models.ForeignKey(PlanoSaude, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.nome} - {self.cidade}"