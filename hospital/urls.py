from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('proximos/', views.listar_hospitais_perto, name='listar_proximos'),
    path('<int:pk>/', views.detalhe_hospital, name='detalhe_hospital'),
]