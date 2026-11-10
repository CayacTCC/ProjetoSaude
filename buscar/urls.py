from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscar_hospitais, name='buscar_hospitais'),
]