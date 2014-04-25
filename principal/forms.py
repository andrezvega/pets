#encoding:utf-8 
from django.forms import ModelForm
from django import forms
from principal.models import Mascotas


class MascotasForm(ModelForm):
    class Meta:
        model = Mascotas


