from django.urls import path
from . import views

urlpatterns = [
    path('agendar/', views.criar_agendamento, name='criar_agendamento_sem_hospital'),
    path('agendar/<int:hospital_id>/', views.criar_agendamento, name='criar_agendamento'),
    path('minhas-consultas/', views.minhas_consultas, name='minhas_consultas'),
    path('cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento'),
    path('api/hospitais/', views.api_hospitais_por_cidade, name='api_hospitais_por_cidade'),
    path('api/exames/<int:hospital_id>/', views.api_exames_por_hospital, name='api_exames_por_hospital'),
]