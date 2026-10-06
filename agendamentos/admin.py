from django.contrib import admin
from .models import Agendamento

@admin.register(Agendamento)
class AgendamentoAdmin(admin.ModelAdmin):
    list_display = ('paciente', 'hospital', 'data_consulta', 'horario_consulta', 'status')
    list_filter = ('status', 'data_consulta', 'hospital')
    search_fields = ('paciente__usuario__first_name', 'paciente__cpf', 'hospital__nome')
    