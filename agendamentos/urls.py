from django.urls import path
from . import views

urlpatterns = [
    path('agendar/<int:hospital_id>/', views.criar_agendamento, name='criar_agendamento'),
    path('minhas-consultas/', views.minhas_consultas, name='minhas_consultas'),
    path('cancelar/<int:agendamento_id>/', views.cancelar_agendamento, name='cancelar_agendamento')
]