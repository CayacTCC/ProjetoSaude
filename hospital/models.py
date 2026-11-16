from django.db import models

class PlanoSaude(models.Model):
    nome = models.CharField(max_length=100)

    class Meta:
        ordering = ['nome']

    def __str__(self): 
        return self.nome

class TipoExame(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Tipos de Exame")

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return self.nome

class Exame(models.Model):
    nome = models.CharField(max_length=100)
    tipo = models.ForeignKey(TipoExame, on_delete=models.CASCADE, related_name='Exames')

    class Meta:
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} ({self.tipo.nome})"

class ExameEspecifico(models.Model):
    nome = models.CharField(max_length=150)
    descricao = models.TextField(blank=True, null=True, verbose_name="Detalhes")
    exame_base = models.ForeignKey(Exame, on_delete=models.CASCADE, related_name="Especificacoes")

    class Meta:
        ordering = ['nome']

    def __str__(self):
        if self.descricao:
            return f"{self.nome} - [{self.descricao}]"
        return f"{self.nome}"

class Hospital(models.Model):
    nome = models.CharField(max_length=150)
    endereco = models.CharField(max_length=255)
    cidade = models.CharField(max_length=100, help_text="Ex: Santos, Guarujá, São Vicente...")
    cep = models.CharField(max_length=9, blank=True, null=True)
    
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)

    planos_aceitos = models.ManyToManyField(PlanoSaude)
    exames_disponiveis = models.ManyToManyField(ExameEspecifico)

    class Meta:
        ordering = ['nome']
    #Vamos englobar hospitais da Baixada Santista, são 9 municípios: Santos, São Vicente, Praia Grande, Guarujá, Bertioga, Peruíbe, Cubatão, Itanhaém e Mongaguá 

    def __str__(self):
        return f"{self.nome} ({self.cidade})"