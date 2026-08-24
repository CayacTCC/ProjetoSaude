from django.contrib import admin
from .models import PlanoSaude, TipoExame, Exame, Hospital

admin.site.register(PlanoSaude)
admin.site.register(TipoExame)
admin.site.register(Exame)
admin.site.register(Hospital)
