#encoding:utf-8 
from django.forms import ModelForm
from django import forms
from principal.models import Mascotas
from principal.models import Pregunta


class MascotasForm(ModelForm):
    class Meta:
        model = Mascotas

class PreguntaForm(ModelForm):
	class Meta:
		model = Pregunta		


