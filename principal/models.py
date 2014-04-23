from django.db import models
from django.contrib.auth.models import User

class Mascotas(models.Model):

	nombre = models.CharField(max_length=150)
	edad = models.DateField()
	usuario = models.ForeignKey(User)			

	def __unicode__(self):
		return self.nombre		
