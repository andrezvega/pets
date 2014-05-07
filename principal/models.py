#encoding:utf-8
from django.db import models
from django.contrib.auth.models import User

class Mascotas(models.Model):

	nombre = models.CharField(max_length=150)
	edad = models.DateField()
	usuario = models.ForeignKey(User)
	tipo = models.IntegerField(max_length=1)
	imagen = models.ImageField(upload_to='imagenMascota', verbose_name='Imágen')			

	def __unicode__(self):
		return self.nombre

class Especialidad(models.Model):
	nombre = models.CharField(max_length=150)

	def __unicode__(self):
		return self.nombre

class Medicos(models.Model):

	cedula = models.CharField(max_length=150)
	nombres = models.CharField(max_length=150)
	apellidos = models.CharField(max_length=150)
	direccion = models.CharField(max_length=150)
	telefono = models.IntegerField(max_length=15)
	imagen = models.ImageField(upload_to='imagenMedico', verbose_name='Imágen')
	especialidad = models.ForeignKey(Especialidad)

	def __unicode__(self):
		return self.cedula

class ComplementoUsuario(models.Model):

	direccion = models.CharField( max_length=150 )  
	telefono = models.IntegerField( max_length=15)
	imagen = models.ImageField(upload_to='imagenUsuario', verbose_name='Imágen')
	usuario = models.ForeignKey(User)

class Pregunta(models.Model):
	pregunta = models.CharField(max_length=250)
	descipcion = models.TextField()
	fecha = models.DateTimeField()
	usuario = models.ForeignKey(User)
	
	def __unicode__(self):
		return self.pregunta

