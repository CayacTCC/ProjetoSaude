from django.db import models
from hospital.models import PlanoSaude

class Paciente(models.Model):
    nome = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=128)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)

    plano_de_saude = models.ForeignKey(PlanoSaude, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nome