from django.db import models
from pacientes.models import Paciente
from hospital.models import Hospital, ExameEspecifico

class Agendamento(models.Model):
    STATUS_CHOICES = [
        ('AGENDADO', 'Agendado'),
        ('REALIZADO', 'Realizado'),
        ('CANCELADO', 'Cancelado'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='agendamentos')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='agendamentos')
    exame_especifico = models.ForeignKey(ExameEspecifico, on_delete=models.SET_NULL, null=True, blank=True)

    data_consulta = models.DateField()
    horario_consulta = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AGENDADO')
    observacoes = models.TextField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        nome_paciente = self.paciente.usuario.first_name if self.paciente.usuario else self.paciente.cpf
        return f"{nome_paciente} - {self.hospital.nome} ({self.data_consulta})"

    class Meta:
        ordering = ['-data_consulta', '-horario_consulta']
