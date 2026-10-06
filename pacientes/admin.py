from django.contrib import admin
from .models import Paciente, HistoricoExame

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('get_nome', 'get_email', 'cpf', 'cidade')
    search_fields = ('usuario__fisrt_name', 'usuario__email', 'cpf')

    @admin.display(ordering='usuario__first_name', description="Nome")
    def get_nome(self, obj):
        return obj.usuario.first_name if obj.usuario else "Sem Nome"

    @admin.display(ordering='usuario__email', description='E-mail')
    def get_email(self, obj):
        return obj.usuario.email if obj.usuario else "Sem E-mail"

@admin.register(HistoricoExame)
class HistoricoExameAdmin(admin.ModelAdmin):
    list_display = ('nome_exame', 'paciente', 'data_realizacao')