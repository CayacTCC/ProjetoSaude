from django.db import models

class PlanoSaude(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self): 
        return self.nome

class TipoExame(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Tipos de Exame")

    def __str__(self):
        return self.nome

class Exame(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoExame, on_delete=models.CASCADE, related_name='Exames')

    def __str__(self):
        return f"{self.nome} ({self.tipo.nome})"

class Hospital(models.Model):
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=255)
    planos_aceitos = models.ManyToManyField(PlanoSaude)
    exames_disponiveis = models.ManyToManyField(Exame)
    #Vamos englobar hospitais da Baixada Santista, são 9 municípios: Santos, São Vicente, Praia Grande, Guarujá, Bertioga, Peruíbe, Cubatão, Itanhaém e Mongaguá 

    def __str__(self):
        return self.nome