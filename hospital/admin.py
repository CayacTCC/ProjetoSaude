from django.contrib import admin
from .models import PlanoSaude, TipoExame, Exame, ExameEspecifico, Hospital

@admin.register(Hospital)
class HospitalAdmin(admin.ModelAdmin):
    list_display = ('nome', 'cidade', 'endereco')
    search_fields = ('nome', 'cidade')

    filter_horizontal = ('planos_aceitos', 'exames_disponiveis')

admin.site.register(PlanoSaude)
admin.site.register(TipoExame)
admin.site.register(Exame)
admin.site.register(ExameEspecifico)
