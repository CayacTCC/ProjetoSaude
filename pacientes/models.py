#Já arrumei

from django.db import models
from django.contrib.auth.models import User
from hospital.models import PlanoSaude

class Paciente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True, related_name='paciente_perfil')

    
    cpf = models.CharField(max_length=14, unique=True)
    telefone = models.CharField(max_length=15, blank=True, null=True)
    data_nascimento = models.DateField(blank=True, null=True)
    
    cep = models.CharField(max_length=9, blank=True, null=True)
    rua = models.CharField(max_length=150, blank=True, null=True)
    bairro = models.CharField(max_length=100, blank=True, null=True)
    cidade = models.CharField(max_length=100, blank=True, null=True)
    uf = models.CharField(max_length=2, blank=True, null=True)

    plano_de_saude = models.ForeignKey(PlanoSaude, on_delete=models.SET_NULL, null=True, blank=True)

    tipo_sanguineo = models.CharField(max_length=3, blank=True, null=True, choices=[
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ])

    doencas_cronicas = models.TextField(blank=True, null=True, help_text="Ex: Asma, Diabetes, Hipertensão")
    medicacoes_uso_continuo = models.TextField(blank=True, null=True, help_text="Ex: Losartana 50mg")

    def __str__(self):
        nome = self.usuario.first_name if self.usuario else "Sem Nome"
        return f"{self.nome} - {self.cidade}"

class HistoricoExame(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name="historico_exames")
    nome_exame = models.CharField(max_length=150)
    data_realizacao = models.DateField()
    local_realizado = models.CharField(max_length=150, blank=True, null=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        nome = self.paciente.usuario.first_name if self.paciente.usuario.first_name else "Sem Nome"
        return f"{self.nome_exame} - Paciente: {nome}"