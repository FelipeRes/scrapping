from django.db import models

# Create your models here.
class ClimaTeresina(models.Model):
	horario = models.DateTimeField(auto_now_add=True)
	atualizacao = models.CharField(max_length=8)
	temperatura = models.CharField(max_length=16)
	sensacao = models.CharField(max_length=16)
	umidade = models.CharField(max_length=16)
	pressao = models.CharField(max_length=16)
	vento = models.CharField(max_length=16)

	def __str__(self):
		return "Dados de teresina em " +str(self.horario) + ". Temperatura: "+str(self.temperatura)
